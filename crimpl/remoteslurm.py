
# from time import sleep as _sleep
import os as _os
import subprocess as _subprocess

from . import common as _common

class RemoteSlurmJob(_common.ServerJob):
    def __init__(self, server=None,
                 job_name=None, nprocs=4,
                 slurm_id=None, connect_to_existing=None):
        """
        Create and submit a job on a <RemoteSlurmServer>.

        Under-the-hood, this creates a subdirectory in <RemoteSlurmServer.directory>
        based on the provided or assigned `job_name`.  All submitted scripts/files
        (through either <RemoteSlurmJob.run_script> or <RemoteSlurmJob.submit_script>)
        are copied to and run in this directory.

        Arguments
        -------------
        * `server` (<RemoteSlurmServer>, optional, default=None): server to
            use when running the job.  If `server` is not provided, `host` must
            be provided.
        * `job_name` (string, optional, default=None): name for this job instance.
            If not provided, one will be created from the current datetime and
            accessible through <RemoteSlurmJob.job_name>.  This `job_name` will
            be necessary to reconnect to a previously submitted job.
        * `nprocs` (int, optional, default=4): default number of procs to use
            when calling <RemoteSlurmJob.submit_job>
        * `slurm_id` (int, optional, default=None): internal id of the remote
            slurm job.  If unknown, this will be determined automatically.
            Do **NOT** set `slurm_id` for a new <RemoteSlurmJob> instance.
        * `connect_to_existing` (bool, optional, default=None): NOT YET IMPLEMENTED
        """
        if slurm_id is not None and not isinstance(slurm_id, int):
            raise TypeError("slurm_id must be of type int")
        # TODO: check if slurm_id and job_name are in agreement? or is this handled by the super call below?
        self._slurm_id = slurm_id


        if connect_to_existing is None:
            if job_name is None:
                connect_to_existing = False
            else:
                connect_to_existing = True

        # run ls on

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

        self._nprocs = nprocs

        super().__init__(server, job_name, job_submitted=connect_to_existing)

    def __repr__(self):
        return "<RemoteSlurmJob job_name={}>".format(self.job_name)

    @property
    def nprocs(self):
        """
        Default number of processors to use when calling <RemoteSlurm.submit_job>.

        Returns
        ---------
        * (int)
        """
        return self._nprocs

    @property
    def slurm_id(self):
        """
        Access the internal remote id of the Slurm scheduler on the remote server.

        Returns
        ----------
        * (int) slurm id
        """
        if self._slurm_id is None:
            # attempt to get slurm id from server
            try:
                out = _subprocess.check_output(self.server.ssh_cmd+" \"cat {}\"".format(_os.path.join(self.remote_directory, "crimpl_slurm_id")), shell=True).decode('utf-8').strip()
                self._slurm_id = int(float(out))
            except:
                raise ValueError("No job has been submitted, call submit_script")

        return self._slurm_id

    @property
    def squeue(self):
        """
        Run and return the results from calling `squeue` on the remote server for
        this job's <RemoteSlurmJob.slurm_id>.

        Returns
        -----------
        * (string)
        """
        return _subprocess.check_output(self.server.ssh_cmd+" \"squeue -j {}\"".format(self.slurm_id), shell=True).decode('utf-8').strip()

    @property
    def job_status(self):
        """
        Return the status of the job by calling and parsing the output of
        <RemoteSlurmJob.squeue>.

        If the job is no longer available in the queue, it is assumed to have
        completed (although in reality, it may have failed or been canceled).

        Returns
        -----------
        * (string): one of not-submitted, pending, running, canceled, failed, complete, unknown
        """
        if not self._job_submitted:
            return 'not-submitted'

        try:
            out = self.squeue
        except:
            # then we'll revert to checking the status file below
            out = ""

        if len(out.split("\n")) < 2:
            # then no longer in the queue, so we'll rely on the status file

            try:
                response = _subprocess.check_output(self.server.ssh_cmd+" \"cat {}\"".format(_os.path.join(self.remote_directory, "crimpl-job.status")), shell=True).decode('utf-8').strip()
            except _subprocess.CalledProcessError:
                return 'unknown'

            if response == 'running':
                # then it started, but is no longer running according to slurm
                return 'failed'

            return response

        status = out.split("\n")[1].split()[4]
        # options for status from man squeue
        # BF  BOOT_FAIL       Job terminated due to launch failure, typically due to a hardware failure (e.g. unable to boot the node or block and the job can not be requeued).
        # CA  CANCELLED       Job was explicitly cancelled by the user or system administrator.  The job may or may not have been initiated.
        # CD  COMPLETED       Job has terminated all processes on all nodes with an exit code of zero.
        # CF  CONFIGURING     Job has been allocated resources, but are waiting for them to become ready for use (e.g. booting).
        # CG  COMPLETING      Job is in the process of completing. Some processes on some nodes may still be active.
        # DL  DEADLINE        Job terminated on deadline.
        # F   FAILED          Job terminated with non-zero exit code or other failure condition.
        # NF  NODE_FAIL       Job terminated due to failure of one or more allocated nodes.
        # OOM OUT_OF_MEMORY   Job experienced out of memory error.
        # PD  PENDING         Job is awaiting resource allocation.
        # PR  PREEMPTED       Job terminated due to preemption.
        # R   RUNNING         Job currently has an allocation.
        # RD  RESV_DEL_HOLD   Job is held.
        # RF  REQUEUE_FED     Job is being requeued by a federation.
        # RH  REQUEUE_HOLD    Held job is being requeued.
        # RQ  REQUEUED        Completing job is being requeued.
        # RS  RESIZING        Job is about to change size.
        # RV  REVOKED         Sibling was removed from cluster due to other cluster starting the job.
        # SI  SIGNALING       Job is being signaled.
        # SE  SPECIAL_EXIT    The job was requeued in a special state. This state can be set by users, typically in EpilogSlurmctld, if the job has terminated with a particular exit value.
        # SO  STAGE_OUT       Job is staging out files.
        # ST  STOPPED         Job has an allocation, but execution has been stopped with SIGSTOP signal.  CPUS have been retained by this job.
        # S   SUSPENDED       Job has an allocation, but execution has been suspended and CPUs have been released for other jobs.
        # TO  TIMEOUT         Job terminated upon reaching its time limit.


        if status in ['R', 'CG']:
            return 'running'
        elif status in ['CD']:
            return 'complete'
        elif status in ['CA']:
            return 'cancelled'
        elif status in ['F', 'DL', 'NF', 'OOM', 'RF', 'RV', 'SE', 'ST', 'S', 'TO']:
            return 'failed'
        elif status in ['PD']:
            return 'pending'

        return status

    def _submit_script_cmds(self, script, files, use_slurm, **slurm_kwargs):
        if isinstance(script, str):
            # TODO: allow for http?
            if not _os.path.isfile(script):
                raise ValueError("cannot find valid script at {}".format(script))

            f = open(script, 'r')
            script = script.readlines()

        if not isinstance(script, list):
            raise TypeError("script must be of type string (path) or list (list of commands)")

        _slurm_kwarg_to_prefix = {'job_name': '-J ',
                                  'nprocs': '-n ',
                                  'walltime': '-t ',
                                  'mail_type': '--mail-type=',
                                  'mail_user': '--mail-user='}

        if use_slurm:
            slurm_script = ["#!/bin/bash"]
            # TODO: use job subdirectory
            slurm_script += ["#SBATCH -D {}".format(self.remote_directory+"/")]
            for k,v in slurm_kwargs.items():
                prefix = _slurm_kwarg_to_prefix.get(k, False)
                if prefix is False:
                    raise NotImplementedError("slurm command for {} not implemented".format(k))
                slurm_script += ["#SBATCH {}{}".format(prefix, v)]

            script = slurm_script + ["\n\n"] + ["echo \'running\' > crimpl-job.status"] + script + ["echo \'complete\' > crimpl-job.status"]

        # TODO: use tmp file instead
        f = open('crimpl_script.sh', 'w')
        f.write("\n".join(script))
        f.close()

        if not isinstance(files, list):
            raise TypeError("files must be of type list")
        for f in files:
            if not _os.path.isfile(f):
                raise ValueError("cannot find file at {}".format(f))

        mkdir_cmd = self.server.ssh_cmd+" \"mkdir -p {}\"".format(self.remote_directory)

        # TODO: use job subdirectory for server_path
        scp_cmd = self.server.scp_cmd_to.format(local_path=" ".join(["crimpl_script.sh"]+files), server_path=self.remote_directory+"/")

        cmd = self.server.ssh_cmd
        # TODO: job subdirectory here
        remote_script = _os.path.join(self.remote_directory, _os.path.basename("crimpl_script.sh"))
        if use_slurm:
            cmd += " \"sbatch {remote_script}\"".format(remote_script=remote_script)
        else:
            cmd += " \"chmod +x {remote_script}; sh {remote_script}\"".format(remote_script=remote_script)

        return [mkdir_cmd, scp_cmd, cmd]

    def run_script(self, script, files=[], trial_run=False):
        """
        Run a script on the server, and wait for it to complete.

        This is useful for short installation/setup scripts that do not belong
        in the scheduled job.

        The resulting `script` and `files` are copied to <RemoteSlurmJob.remote_directory>
        on the remote server and then `script` is executed via ssh.

        See <RemoteSlurmJob.submit_script> to submit a script via the slurm scheduler
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
        cmds = self._submit_script_cmds(script, files, use_slurm=False)
        if trial_run:
            return cmds

        for cmd in cmds:
            print("running: {}".format(cmd))

            # TODO: get around need to add IP to known hosts (either by
            # expecting and answering yes, or by looking into subnet options)
            _os.system(cmd)

        return

    def submit_script(self, script, files=[],
                      job_name=None,
                      nprocs=None,
                      walltime='2-00:00:00',
                      mail_type='END,FAIL',
                      mail_user=None,
                      wait_for_job_status=False,
                      trial_run=False):
        """
        Submit a script to the server.

        This will copy `script` (modified with the provided slurm options) and
        `files` to <RemoteSlurmJob.remote_directory> on the remote server and
        submit the script to the slurm scheduler.  To check on its status,
        see <RemoteSlurmJob.job_status>.

        Additional slurm customization (not included in the keyword arguments
        listed below) can be included in the beginning of the script.

        To check on any expected output files, call <RemoteSlurmJob.check_output>.

        See <RemoteSlurmJob.run_script> to run a script and wait for it to complete.

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
        * `job_name` (string, optional, default=None): name of the job within slurm.
            Prepended to `script` as "#SBATCH -J jobname".  Defaults to
            <RemoteSlurmJob.job_name>.
        * `nprocs` (int, optional, default=None): number of processors to run the
            job.  Prepended to `script` as "#SBATCH -n nprocs".  If None, will
            default to the `nprocs` set when creating the <RemoteSlurmJob> instance.
            See <RemoteSlurmJob.nprocs>.
        * `walltime` (string, optional, default='2-00:00:00'): maximum walltime
            to schedule the job.  Prepended to `script` as "#SBATCH -t walltime".
        * `mail_type` (string, optional, default='END,FAIL'): conditions to notify
            by email to `mail_user`.  Prepended to `script` as "#SBATCH --mail_user=mail_user".
        * `mail_user` (string, optional, default=None): email to send notifications.
            Prepended to `script` as "#SBATCH --mail_user=mail_user"
        * `wait_for_job_status` (bool or string or list, optional, default=False):
            Whether to wait for a specific job_status.  If True, will default to
            'complete'.  See also <RemoteSlurmJob.wait_for_job_status>.
        * `trial_run` (bool, optional, default=False): if True, the commands
            that would be sent to the server are returned but not executed.

        Returns
        ------------
        * <RemoteSlurmJob>

        Raises
        ------------
        * ValueError: if a script has already been submitted within this
            <RemoteSlurmJob> instance.  To run another script, call <RemoteSlurmJob.release_job>
            or create another <RemoteSlurmJob> instance.
        * TypeError: if `script` or `files` are not valid types.
        * ValueError: if the files referened by `script` or `files` are not valid.
        """
        if self._slurm_id is not None:
            raise ValueError("a job is already submitted.  Use a new instance to run multiple jobs, or call release_job() to stop tracking slurm_id={}".format(self.slurm_id))

        if nprocs is None:
            nprocs = self.nprocs

        cmds = self._submit_script_cmds(script, files, use_slurm=True,
                                        job_name=job_name if job_name is not None else self.job_name,
                                        nprocs=nprocs,
                                        walltime=walltime,
                                        mail_type=mail_type,
                                        mail_user=mail_user)
        if trial_run:
            return cmds

        for cmd in cmds:
            print("running: {}".format(cmd))

            # TODO: get around need to add IP to known hosts (either by
            # expecting and answering yes, or by looking into subnet options)
            # _os.system(cmd)

            out = _subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
            print(out)
            if "sbatch" in cmd:
                self._slurm_id = out.split(' ')[-1]

                # leave record of slurm id in the remote directory
                _os.system(self.server.ssh_cmd+" \"echo {} > {}\"".format(self._slurm_id, _os.path.join(self.remote_directory, "crimpl_slurm_id")))


        self._job_submitted = True

        if wait_for_job_status:
            self.wait_for_job_status(wait_for_job_status)

        return self

    def check_output(self, server_path, local_path="./",
                     wait_for_output=False):
        """
        Attempt to copy a file back from the server.

        Arguments
        -----------
        * `server_path` (string or list): path(s) (relative to `directory`) on the server
            of the file(s) to retrieve.
        * `local_path` (string, optional, default="./"): local path to copy
            the retrieved file.
        * `wait_for_output` (bool, optional, default=False): NOT IMPLEMENTED


        Returns
        ----------
        * None
        """
        if wait_for_output:
            raise NotImplementedError("wait_for_output not yet implemented")

        if isinstance(server_path, str):
            server_path_str = _os.path.join(self.remote_directory, server_path)
        else:
            server_path = [_os.path.join(self.remote_directory, path) for path in server_path]
            server_path_str = "\"{}\"".format(" ".join(server_path))

        scp_cmd = self.server.scp_cmd_from.format(server_path=server_path_str, local_path=local_path)
        # TODO: execute cmd, handle wait_for_output and also handle errors if stopped/terminated before getting results
        print("running: {}".format(scp_cmd))
        _os.system(scp_cmd)



class RemoteSlurmServer(_common.Server):
    _JobClass = RemoteSlurmJob
    def __init__(self, host, directory=None, server_name=None):
        """
        Connect to a remote server running a Slurm scheduler.

        To create a new job, use <RemoteSlurmServer.create_job> or to connect
        to a previously created job, use <RemoteSlurmServer.get_job>.

        Arguments
        -----------
        * `host` (string): host of the remote server.  Must be passwordless ssh-able.
            See <RemoteSlurmServer.host>
        * `directory` (string, optional, default=None): root directory of all
            jobs to run on the remote server.  The directory will be created
            if it does not already exist.
        * `server_name` (string): name to assign to the server.  If not provided,
            will be adopted automatically from `host` and available from
            <RemoteSlurmServer.server_name>.
        """
        self._host = host

        if server_name is None:
            server_name = host.split("@")[-1]

        self._server_name = server_name

        super().__init__(directory)

    @classmethod
    def load(cls, name):
        raise NotImplementedError()

    def __repr__(self):
        return "<RemoteSlurmServer host={} directory={}>".format(self.config.host, self.config.directory)

    @property
    def server_name(self):
        """
        internal name of the server.

        Returns
        ----------
        * (string)
        """
        return self._server_name

    @property
    def host(self):
        """
        host of the remote machine.  Should be passwordless ssh-able for the current user

        Returns
        ---------
        * (string)
        """
        return self._host

    @property
    def ssh_cmd(self):
        """
        ssh command to the server

        Returns
        ----------
        * (string)
        """

        return "ssh {}".format(self.host)

    @property
    def scp_cmd_to(self):
        """
        scp command to copy files to the server.

        Returns
        ----------
        * (string): command with "{}" placeholders for `local_path` and `server_path`.
        """

        return "scp {local_path} %s:{server_path}" % (self.host)

    @property
    def scp_cmd_from(self):
        """
        scp command to copy files from the server.

        Returns
        ----------
        * (string): command with "{}" placeholders for `server_path` and `local_path`.
        """

        return "scp %s:{server_path} {local_path}" % (self.host)

    @property
    def squeue(self):
        """
        Run and return the output of `squeue` on the server (for all jobs).

        To run for a single job, see <RemoteSlurmJob.squeue>.

        Returns
        -----------
        * (string)
        """
        return _subprocess.check_output(self.ssh_cmd+" \"squeue\"", shell=True).decode('utf-8').strip()

    @property
    def sinfo(self):
        """
        Run and return the output of `sinfo` on the server (for all jobs).

        Returns
        -----------
        * (string)
        """
        return _subprocess.check_output(self.ssh_cmd+" \"sinfo\"", shell=True).decode('utf-8').strip()

    @property
    def ls(self):
        """
        Run and return the output of `ls` on the server (for all jobs).

        Returns
        -----------
        * (string)
        """
        return _subprocess.check_output(self.ssh_cmd+" \"ls\"", shell=True).decode('utf-8').strip()

    def create_job(self, job_name=None, nprocs=4):
        """
        Create a child <RemoteSlurmJob> instance.

        Arguments
        -----------
        * `job_name` (string, optional, default=None): name for this job instance.
            If not provided, one will be created from the current datetime and
            accessible through <RemoteSlurmJob.job_name>.  This `job_name` will
            be necessary to reconnect to a previously submitted job.
        * `nprocs` (int, optional, default=4): default number of procs to use
            when calling <RemoteSlurmJob.submit_job>

        Returns
        ---------
        * <RemoteSlurmJob>
        """
        return self._JobClass(server=self, job_name=job_name,
                              nprocs=nprocs, connect_to_existing=False)

    def _submit_script_cmds(self, script, files):
        if isinstance(script, str):
            # TODO: allow for http?
            if not _os.path.isfile(script):
                raise ValueError("cannot find valid script at {}".format(script))

            f = open(script, 'r')
            script = script.readlines()

        if not isinstance(script, list):
            raise TypeError("script must be of type string (path) or list (list of commands)")

        # TODO: use tmp file instead
        f = open('crimpl_script.sh', 'w')
        f.write("\n".join(script))
        f.close()

        if not isinstance(files, list):
            raise TypeError("files must be of type list")
        for f in files:
            if not _os.path.isfile(f):
                raise ValueError("cannot find file at {}".format(f))

        mkdir_cmd = self.ssh_cmd+" \"mkdir -p {}\"".format(self.directory)

        # TODO: use job subdirectory for server_path
        scp_cmd = self.scp_cmd_to.format(local_path=" ".join(["crimpl_script.sh"]+files), server_path=self.directory+"/")

        cmd = self.ssh_cmd
        # TODO: job subdirectory here
        remote_script = _os.path.join(self.directory, _os.path.basename("crimpl_script.sh"))
        cmd += " \"chmod +x {remote_script}; sh {remote_script}\"".format(remote_script=remote_script)

        return [mkdir_cmd, scp_cmd, cmd]

    def run_script(self, script, files=[], trial_run=False):
        """
        Run a script on the server, and wait for it to complete.

        The files are copied and executed in <RemoteSlurmServer.directory> directly
        (whereas <RemoteSlurmJob> scripts are executed in subdirectories).

        This is useful for short installation/setup scripts that do not belong
        in the scheduled job.

        The resulting `script` and `files` are copied to <RemoteSlurmServer.directory>
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
        cmds = self._submit_script_cmds(script, files, use_slurm=False)
        if trial_run:
            return cmds

        for cmd in cmds:
            print("running: {}".format(cmd))

            # TODO: get around need to add IP to known hosts (either by
            # expecting and answering yes, or by looking into subnet options)
            _os.system(cmd)

        return
