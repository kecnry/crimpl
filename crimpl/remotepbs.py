
# from time import sleep as _sleep
import os as _os
import subprocess as _subprocess

from . import common as _common
from . import remotethread as _remotethread

class RemotePBSJob(_remotethread.RemoteThreadJob):
    def __init__(self, server=None,
                 job_name=None,
                 conda_env=None, isolate_env=False,
                 nnodes=1, nprocs=4,
                 pbs_id=None, connect_to_existing=None):
        """
        Create and submit a job on a <RemotePBSServer>.

        Under-the-hood, this creates a subdirectory in <RemotePBSServer.directory>
        based on the provided or assigned `job_name`.  All submitted scripts/files
        (through either <RemotePBSJob.run_script> or <RemotePBSJob.submit_script>)
        are copied to and run in this directory.

        Arguments
        -------------
        * `server` (<RemotePBSServer>, optional, default=None): server to
            use when running the job.  If `server` is not provided, `host` must
            be provided.
        * `job_name` (string, optional, default=None): name for this job instance.
            If not provided, one will be created from the current datetime and
            accessible through <RemotePBSJob.job_name>.  This `job_name` will
            be necessary to reconnect to a previously submitted job.
        * `conda_env` (string or None, optional, default=None): name of
            the conda environment to use for the job or False to not use a
            conda environment.  If not passed or None, will default to 'default'
            if conda is installed on the server or to False otherwise.
        * `isolate_env` (bool, optional, default=False): whether to clone
            the `conda_env` for use in this job.  If True, any setup/installation
            done by this job will not affect the original environment and
            will not affect other jobs.  Note that the environment is cloned
            (and therefore isolated) at the first call to <<class>.run_script>
            or <<class>.submit_script>.  Setup in the parent environment can
            be done at the server level, but requires passing `conda_env`.
            Will raise an error if `isolate_env=True` and `conda_env=False`.
        * `nnodes` (int, optional, default=1): default number of nodes to use
            when calling <RemotePBSJob.submit_script>
        * `nprocs` (int, optional, default=4): default number of procs to use
            when calling <RemotePBSJob.submit_script>
        * `pbs_id` (int, optional, default=None): internal id of the remote
            PBS job.  If unknown, this will be determined automatically.
            Do **NOT** set `pbs_id` for a new <RemotePBSJob> instance.
        * `connect_to_existing` (bool, optional, default=None): NOT YET IMPLEMENTED
        """
        if pbs_id is not None and not isinstance(pbs_id, int):
            raise TypeError("pbs_id must be of type int")
        # TODO: check if pbs_id and job_name are in agreement? or is this handled by the super call below?
        self._pbs_id = pbs_id


        if connect_to_existing is None:
            if job_name is None:
                connect_to_existing = False
            else:
                connect_to_existing = True

        job_matches = [j for j in server.existing_jobs if j == job_name or job_name is None]

        if connect_to_existing:
            if len(job_matches) == 1:
                job_name = job_matches[0]
            elif len(job_matches) > 1:
                raise ValueError("{} jobs found on {} server.  Provide job_name or create a new job".format(len(job_matches), server.server_name))
            else:
                raise ValueError("no job could be found with job_name={} on {} server".format(job_name, server.server_name))
        else:
            if job_name is None:
                job_name = _common._new_job_name()
            elif len(job_matches):
                raise ValueError("job_name={} already exists on {} server".format(job_name, server.server_name))

        self._nnodes = nnodes
        self._nprocs = nprocs

        super().__init__(server, job_name,
                         conda_env=conda_env,
                         isolate_env=isolate_env,
                         connect_to_existing=connect_to_existing)

    @property
    def nnodes(self):
        """
        Default number of nodes to use when calling <<class>.submit_script>.

        Returns
        ----------
        * (int)
        """
        return self._nnodes

    @property
    def nprocs(self):
        """
        Default number of processors to use when calling <<class>.submit_script>.

        Returns
        ---------
        * (int)
        """
        return self._nprocs

    @property
    def pbs_id(self):
        """
        Access the internal remote id of the PBS scheduler on the remote server.

        Returns
        ----------
        * (int) pbs id
        """
        if self._pbs_id is None:
            # attempt to get pbs id from server
            try:
                out = self.server._run_server_cmd("cat {}".format(_os.path.join(self.remote_directory, "crimpl_pbs_id")))
                self._pbs_id = int(float(out))
            except:
                raise ValueError("No job has been submitted, call submit_script")

        return self._pbs_id

    @property
    def qstat(self):
        """
        Run and return the results from calling `qstat` on the remote server for
        this job's <RemotePBSJob.pbs_id>.

        Returns
        -----------
        * (string)
        """
        return self.server._run_server_cmd("qstat -f {}".format(self.pbs_id))

    @property
    def job_status(self):
        """
        Return the status of the job by calling and parsing the output of
        <RemotePBSJob.qstat>.

        If the job is no longer available in the queue, it is assumed to have
        completed (although in reality, it may have failed or been canceled).

        Returns
        -----------
        * (string): one of not-submitted, pending, running, canceled, failed, complete, unknown
        """
        if not self._job_submitted:
            return 'not-submitted'

        try:
            out = self.qstat
        except:
            # then we'll revert to checking the status file below
            out = ""

        if len(out.split("\n")) < 2:
            # then no longer in the queue, so we'll rely on the status file

            try:
                response = self.server._run_server_cmd("cat {}".format(_os.path.join(self.remote_directory, "crimpl-job.status")))
            except _subprocess.CalledProcessError:
                return 'unknown'

            if response == 'running':
                # then it started, but is no longer running according to PBS
                return 'failed'

            return response


        # TODO: need to find correct format to split line for PBS
        status = out.split("\n")[1].split()[4]
        # options for status from man qstat (http://gridscheduler.sourceforge.net/htmlman/htmlman1/qstat.html)
        # the status of the  parallel  task  -  one  of  r(unning),
        # R(estarted),   s(uspended),   S(uspended),   T(hreshold),
        # w(aiting), h(old), or x(exited).


        if status in ['r', 'R', 'CG']:
            return 'running'
        elif status in ['X']:
            return 'complete'
        elif status in ['s', 'S', 'T']:
            return 'failed'
        elif status in ['w', 'h']:
            return 'pending'

        return status

    def kill_job(self):
        """
        Kill a job by calling `qdel` on the remote server for
        this job's <RemotePBSJob.pbs_id>.

        Returns
        -----------
        * (string)
        """
        return self.server._run_server_cmd("qdel {}".format(self.pbs_id))

    def run_script(self, script, files=[], trial_run=False):
        """
        Run a script on the server in the <<class>.conda_env>,
        and wait for it to complete.

        This is useful for short installation/setup scripts that do not belong
        in the scheduled job.

        The resulting `script` and `files` are copied to <RemotePBSJob.remote_directory>
        on the remote server and then `script` is executed via ssh.

        See <RemotePBSJob.submit_script> to submit a script via the PBS scheduler
        and leave running in the background on the server.

        Arguments
        ----------------
        * `script` (string or list): shell script to run on the remote server,
            including any necessary installation steps.  Note that the script
            can call any other scripts in `files`.  If a string, must be the
            path of a valid file which will be copied to the server.  If a list,
            must be a list of commands (i.e. a newline will be placed between
            each item in the list and sent as a single script to the server).
        * `files` (list, optional, default=[]): list of paths to additional files
            to copy to the server required in order to successfully execute
            `script`.
        * `trial_run` (bool, optional, default=False): if True, the commands
            that would be sent to the server are returned but not executed.


        Returns
        ------------
        * None

        Raises
        ------------
        * TypeError: if `script` or `files` are not valid types.
        * ValueError: if the files referened by `script` or `files` are not valid.
        """
        return super().run_script(script, files=files, trial_run=trial_run)

    def submit_script(self, script, files=[],
                      pbs_job_name=None,
                      nnodes=1,
                      nprocs=None,
                      walltime='2-00:00:00',
                      mail_type='ae',
                      mail_user=None,
                      ignore_files=[],
                      wait_for_job_status=False,
                      trial_run=False):
        """
        Submit a script to the server in the <<class>.conda_env>.

        This will copy `script` (modified with the provided PBS options) and
        `files` to <RemotePBSJob.remote_directory> on the remote server and
        submit the script to the PBS scheduler.  To check on its status,
        see <RemotePBSJob.job_status>.

        Additional PBS customization (not included in the keyword arguments
        listed below) can be included in the beginning of the script.

        To check on any expected output files, call <RemotePBSJob.check_output>.

        See <RemotePBSJob.run_script> to run a script and wait for it to complete.

        Arguments
        ----------------
        * `script` (string or list): shell script to run on the remote server,
            including any necessary installation steps.  Note that the script
            can call any other scripts in `files`.  If a string, must be the
            path of a valid file which will be copied to the server.  If a list,
            must be a list of commands (i.e. a newline will be placed between
            each item in the list and sent as a single script to the server).
        * `files` (list, optional, default=[]): list of paths to additional files
            to copy to the server required in order to successfully execute
            `script`.
        * `pbs_job_name` (string, optional, default=None): name of the job within PBS.
            Prepended to `script` as "#PBS -N jobname".  Defaults to
            <RemotePBSJob.job_name>.
        * `nnodes` (int, optional, default=1): number of nodes to run the
            job.  Prepended to `script` as "#PBS -l nodes=nnodes".
        * `nprocs` (int, optional, default=None): number of processors (per node) to run the
            job.  Prepended to `script` as "#PBS -l ppn=nprocs".  If None, will
            default to the `nprocs` set when creating the <RemotePBSJob> instance.
            See <RemotePBSJob.nprocs>.
        * `walltime` (string, optional, default='2-00:00:00'): maximum walltime
            to schedule the job.  Prepended to `script` as "#PBS -l walltime=walltime".
        * `mail_type` (string, optional, default='ae'): conditions to notify
            by email to `mail_user`.  Prepended to `script` as "#PBS -m mail_type".
        * `mail_user` (string, optional, default=None): email to send notifications.
            If not provided or None, will default to the value in <RemotePBSServer.mail_user>.
            Prepended to `script` as "#PBS -M mail_user"
        * `ignore_files` (list, optional, default=[]): list of filenames on the
            remote server to ignore when calling <<class>.check_output>
        * `wait_for_job_status` (bool or string or list, optional, default=False):
            Whether to wait for a specific job_status.  If True, will default to
            'complete'.  See also <RemotePBSJob.wait_for_job_status>.
        * `trial_run` (bool, optional, default=False): if True, the commands
            that would be sent to the server are returned but not executed.

        Returns
        ------------
        * <RemotePBSJob>

        Raises
        ------------
        * ValueError: if a script has already been submitted within this
            <RemotePBSJob> instance.
        * TypeError: if `script` or `files` are not valid types.
        * ValueError: if the files referened by `script` or `files` are not valid.
        """
        if self._pbs_id is not None:
            raise ValueError("a job is already submitted.")

        if nprocs is None:
            nprocs = self.nprocs

        if "crimpl_submit_script.sh" in self.ls:
            raise ValueError("job already submitted.  Create a new job or call resubmit_job")

        cmds = self.server._submit_script_cmds(script, files, ignore_files,
                                               use_scheduler='pbs',
                                               directory=self.remote_directory,
                                               conda_env=self.conda_env,
                                               isolate_env=self.isolate_env,
                                               job_name=pbs_job_name if pbs_job_name is not None and len(pbs_job_name) else self.job_name,
                                               terminate_on_complete=False,
                                               use_nohup=False,
                                               install_conda=False,
                                               #nnodes=nnodes,
                                               nprocs=nprocs,
                                               walltime=walltime,
                                               mail_type=mail_type,
                                               mail_user=mail_user if mail_user is not None else self.server.mail_user)

        if trial_run:
            return cmds

        for cmd in cmds:
            if cmd is None: continue
            # TODO: get around need to add IP to known hosts (either by
            # expecting and answering yes, or by looking into subnet options)

            out = _common._run_cmd(cmd)
            if "qsub" in cmd:
                # TODO: confirm qsub returns the id
                self._pbs_id = out.split(' ')[-1]

                # leave record of pbs id in the remote directory
                self.server._run_server_cmd("echo {} > {}".format(self._pbs_id, _os.path.join(self.remote_directory, "crimpl_pbs_id")))


        self._job_submitted = True
        self._input_files = None

        if wait_for_job_status:
            self.wait_for_job_status(wait_for_job_status)

        return self

    def resubmit_script(self):
        """
        Resubmit an existing job script if <<class>.job_status> one of: complete,
        failed, killed.
        """
        status = self.job_status
        if status not in ['complete', 'failed', 'killed']:
            raise ValueError("cannot resubmit script with job_status='{}'".format(status))

        # NOTE: PBS uses the submission directory as the working directory, so we MUST cd to it instead of just call the full path
        out = self.server._run_server_cmd("cd {} && qsub {remote_script}".format(self.remote_directory, remote_script="crimple_submit_script.sh"))
        # TODO: confirm qsub returns the id
        self._pbs_id = out.split(' ')[-1]

        # leave record of (NEW) pbs id in the remote directory
        self.server._run_server_cmd("echo {} > {}".format(self._pbs_id, _os.path.join(self.remote_directory, "crimpl_pbs_id")))




class RemotePBSServer(_remotethread.RemoteThreadServer):
    _JobClass = RemotePBSJob
    def __init__(self, host, directory='~/crimpl', ssh='ssh', scp='scp',
                 mail_user=None, server_name=None):
        """
        Connect to a remote server running a PBS scheduler.

        To create a new job, use <RemotePBSServer.create_job> or to connect
        to a previously created job, use <RemotePBSServer.get_job>.

        Arguments
        -----------
        * `host` (string): host of the remote server.  Must be passwordless ssh-able.
            See <RemotePBSServer.host>
        * `directory` (string, optional, default='~/crimpl'): root directory of all
            jobs to run on the remote server.  The directory will be created
            if it does not already exist.
        * `ssh` (string, optional, default='ssh'): command (and any arguments in
            addition to `host`) to ssh to the remote server.
        * `scp` (string, optional, default='scp'): command (and any arguments)
            to copy files to the remote server.
        * `mail_user` (string, optional, default=None): email to send notifications.
            If not provided or None, will default to the value in <RemotePBSServer.mail_user>.
            Prepended to `script` as "#PBS -M mail_user"
        * `server_name` (string): name to assign to the server.  If not provided,
            will be adopted automatically from `host` and available from
            <RemotePBSServer.server_name>.
        """
        super().__init__(host, directory, ssh, scp)
        self.mail_user = mail_user
        self._dict_keys += ['mail_user']

    @property
    def mail_user(self):
        """
        Default email to send notification from the PBS scheduler when calling
        <RemotePBSServer.submit_job> or <RemotePBSJob.submit_script>.
        """
        return self._mail_user

    @mail_user.setter
    def mail_user(self, mail_user):
        if mail_user is None:
            self._mail_user = None
            return

        if not isinstance(mail_user, str):
            raise TypeError("mail_user must be a string or None")

        if "@" not in mail_user:
            raise ValueError("mail_user must be a valid email address (with an @ symbol)")

        self._mail_user = mail_user

    @property
    def qstat(self):
        """
        Run and return the output of `qstat` on the server (for all jobs).

        To run for a single job, see <RemotePBSJob.qstat>.

        Returns
        -----------
        * (string)
        """
        return self._run_server_cmd("qstat")

    @property
    def pbsnodes(self):
        """
        Run and return the output of `pbsnodes` on the server (for all jobs).

        Returns
        -----------
        * (string)
        """
        return self._run_server_cmd("pbsnodes")

    def create_job(self, job_name=None,
                   conda_env=None, isolate_env=False,
                   nnodes=1, nprocs=4):
        """
        Create a child <RemotePBSJob> instance.

        Arguments
        -----------
        * `job_name` (string, optional, default=None): name for this job instance.
            If not provided, one will be created from the current datetime and
            accessible through <RemotePBSJob.job_name>.  This `job_name` will
            be necessary to reconnect to a previously submitted job.
        * `conda_env` (string or None, optional, default=None): name of
            the conda environment to use for the job or False to not use a
            conda environment.  If not passed or None, will default to 'default'
            if conda is installed on the server or to False otherwise.
        * `isolate_env` (bool, optional, default=False): whether to clone
            the `conda_env` for use in this job.  If True, any setup/installation
            done by this job will not affect the original environment and
            will not affect other jobs.  Note that the environment is cloned
            (and therefore isolated) at the first call to <<class>.run_script>
            or <<class>.submit_script>.  Setup in the parent environment can
            be done at the server level, but requires passing `conda_env`.
            Will raise an error if `isolate_env=True` and `conda_env=False`.
        * `nnodes` (int, optional, default=1): default number of nodes to use
            when calling <RemotePBSJob.submit_job>
        * `nprocs` (int, optional, default=4): default number of procs to use
            when calling <RemotePBSJob.submit_job>

        Returns
        ---------
        * <RemotePBSJob>
        """
        return self._JobClass(server=self, job_name=job_name,
                              conda_env=conda_env,
                              isolate_env=isolate_env,
                              nnodes=nnodes, nprocs=nprocs, connect_to_existing=False)

    def submit_job(self, script, files=[],
                   job_name=None, pbs_job_name=None,
                   conda_env=None, isolate_env=False,
                   nnodes=1,
                   nprocs=4,
                   walltime='2-00:00:00',
                   mail_type='END,FAIL',
                   mail_user=None,
                   ignore_files=[],
                   wait_for_job_status=False,
                   trial_run=False):
        """
        Shortcut to <RemotePBSServer.create_job> followed by <RemotePBSJob.submit_script>.

        Arguments
        --------------
        * `script`: passed to <RemotePBSJob.submit_script>
        * `files`: passed to <RemotePBSJob.submit_script>
        * `job_name`: passed to <RemotePBSServer.create_job>
        * `pbs_job_name`: passed to <RemotePBSJob.submit_script>
        * `conda_env`: passed to <RemotePBSServer.create_job>
        * `isolate_env`: passed to <RemotePBSServer.create_job>
        * `nnodes`: passed to <RemotePBSServer.create_job>
        * `nprocs`: passed to <RemotePBSServer.create_job>
        * `walltime`: passed to <RemotePBSJob.submit_script>
        * `mail_type`: passed to <RemotePBSJob.submit_script>
        * `mail_user`: passed to <RemotePBSJob.submit_script>
        * `ignore_files`: passed to <RemotePBSJob.submit_script>
        * `wait_for_job_status`: passed to <RemotePBSJob.submit_script>
        * `trial_run`: passed to <RemotePBSJob.submit_script>

        Returns
        --------------
        * <RemotePBSJob>
        """
        j = self.create_job(job_name=job_name,
                            conda_env=conda_env,
                            isolate_env=isolate_env,
                            nnodes=nnodes,
                            nprocs=nprocs)

        return j.submit_script(script, files=files,
                               pbs_job_name=pbs_job_name,
                               walltime=walltime,
                               mail_type=mail_type,
                               mail_user=mail_user,
                               ignore_files=ignore_files,
                               wait_for_job_status=wait_for_job_status,
                               trial_run=trial_run)

    def run_script(self, script, files=[], conda_env=None, trial_run=False):
        """
        Run a script on the server in the `conda_env`, and wait for it to complete.

        The files are copied and executed in <RemotePBSServer.directory> directly
        (whereas <RemotePBSJob> scripts are executed in subdirectories).

        This is useful for short installation/setup scripts that do not belong
        in the scheduled job.

        The resulting `script` and `files` are copied to <RemotePBSServer.directory>
        on the remote server and then `script` is executed via ssh.

        Arguments
        ----------------
        * `script` (string or list): shell script to run on the remote server,
            including any necessary installation steps.  Note that the script
            can call any other scripts in `files`.  If a string, must be the
            path of a valid file which will be copied to the server.  If a list,
            must be a list of commands (i.e. a newline will be placed between
            each item in the list and sent as a single script to the server).
        * `files` (list, optional, default=[]): list of paths to additional files
            to copy to the server required in order to successfully execute
            `script`.
        * `conda_env` (string or None, optional, default=None): name of
            the conda environment to run the script or False to not use a
            conda environment.  If not passed or None, will default to 'default'
            if conda is installed on the server or to False otherwise.
        * `trial_run` (bool, optional, default=False): if True, the commands
            that would be sent to the server are returned but not executed.


        Returns
        ------------
        * None

        Raises
        ------------
        * TypeError: if `script` or `files` are not valid types.
        * ValueError: if the files referened by `script` or `files` are not valid.
        """
        return super().run_script(script, files=files, conda_env=conda_env, trial_run=trial_run)
