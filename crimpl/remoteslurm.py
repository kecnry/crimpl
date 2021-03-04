
from time import sleep as _sleep
import os as _os
import subprocess as _subprocess

from . import common as _common


class RemoteSlurmConfig(object):
    def __init__(self, host, directory='~/'):
        self.host = host
        self.directory = directory

class RemoteSlurm(_common.ServerJob):
    def __init__(self, config=None, host=None, directory=None,
                 job_name=None, slurm_id=None, connect_to_existing=None):
        """
        Connect to a remote server

        Arguments
        -------------
        * `config`
        * `host`
        * `directory`
        * `job_name`
        * `slurm_id`
        * `connect_to_existing` (bool, optional, default=None): NOT YET IMPLEMENTED
        """
        # TODO: validate config
        if config is None:
            config =  RemoteSlurmConfig(host, directory)

        if host is not None:
            # TODO: make a deepcopy of config first to avoid editing to user copy?
            config.host = host

        if slurm_id is not None and not isinstance(slurm_id, int):
            raise TypeError("slurm_id must be of type int")
        self._slurm_id = slurm_id

        super().__init__(config, job_name, directory, connect_to_existing)

    @property
    def config(self):
        """
        <RemoteSlurmConfig>

        Returns
        ----------
        * <RemoteSlurmConfig>
        """

        return self._config

    @property
    def ssh_cmd(self):
        """
        ssh command to the server

        Returns
        ----------
        * (string)
        """

        return "ssh {}".format(self.config.host)

    @property
    def scp_cmd_to(self):
        """
        scp command to copy files to the server.

        Returns
        ----------
        * (string): command with "{}" placeholders for `local_path` and `server_path`.
        """

        return "scp {local_path} %s:{server_path}" % (self.config.host)

    @property
    def scp_cmd_from(self):
        """
        scp command to copy files from the server.

        Returns
        ----------
        * (string): command with "{}" placeholders for `server_path` and `local_path`.
        """

        return "scp %s:{server_path} {local_path}" % (self.config.host)

    @property
    def slurm_id(self):
        """
        """
        if self._slurm_id is None:
            # attempt to get slurm id from server
            try:
                out = _subprocess.check_output(self.ssh_cmd+" \"cat {}\"".format(_os.path.join(self.remote_directory, "crimpl_slurm_id")), shell=True).decode('utf-8').strip()
                self._slurm_id = int(float(out))
            except:
                raise ValueError("No job has been submitted, call submit_script")

        return self._slurm_id

    @property
    def squeue(self):
        return _subprocess.check_output(self.ssh_cmd+" \"squeue -j {}\"".format(self.slurm_id), shell=True).decode('utf-8').strip()

    @property
    def job_status(self):
        try:
            out = self.squeue
        except:
            # then no longer in the queue, so either invalid, complete, or failed
            return 'complete'
        # print(out)

        # TODO: parse into something useful
        return out

    def release_job(self):
        # stop tracking this job and allow submitting another
        self._slurm_id = None

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

            script = slurm_script + ["\n\n"] + script

        # TODO: use tmp file instead
        f = open('crimpl_script.sh', 'w')
        f.write("\n".join(script))
        f.close()

        if not isinstance(files, list):
            raise TypeError("files must be of type list")
        for f in files:
            if not _os.path.isfile(f):
                raise ValueError("cannot find file at {}".format(f))

        mkdir_cmd = self.ssh_cmd+" \"mkdir -p {}\"".format(self.remote_directory)

        # TODO: use job subdirectory for server_path
        scp_cmd = self.scp_cmd_to.format(local_path=" ".join(["crimpl_script.sh"]+files), server_path=self.remote_directory+"/")

        cmd = self.ssh_cmd
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

        See <RemoteSlurm.submit_script> to submit a script via the slurm scheduler
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
                      nprocs=4,
                      walltime='2-00:00:00',
                      mail_type='END,FAIL',
                      mail_user=None,
                      trial_run=False):
        """
        Submit a script to the server.

        This will copy `script` (modified with the provided slurm options) and
        `files` to the server and submit the script to the slurm scheduler.

        Additional slurm customization (not included in the keyword arguments
        listed below) can be included in the beginning of the script.

        To check on any expected output files, call <RemoteSlurm.check_output>.

        See <RemoteSlurm.run_script> to run a script and wait for it to complete.

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
            <RemoteSlurm.job_name>.
        * `nprocs` (int, optional, default=4): number of processors to run the
            job.  Prepended to `script` as "#SBATCH -n nprocs".
        * `walltime` (string, optional, default='2-00:00:00'): maximum walltime
            to schedule the job.  Prepended to `script` as "#SBATCH -t walltime".
        * `mail_type` (string, optional, default='END,FAIL'): conditions to notify
            by email to `mail_user`.  Prepended to `script` as "#SBATCH --mail_user=mail_user".
        * `mail_user` (string, optional, default=None): email to send notifications.
            Prepended to `script` as "#SBATCH --mail_user=mail_user"
        * `trial_run` (bool, optional, default=False): if True, the commands
            that would be sent to the server are returned but not executed.

        Returns
        ------------
        * (int): <RemoteSlurm.slurm_id>

        Raises
        ------------
        * ValueError: if a script has already been submitted within this
            <RemoteSlurm> instance.  To run another script, call <RemoteSlurm.release_job>
            or create another <RemoteSlurm> instance.
        * TypeError: if `script` or `files` are not valid types.
        * ValueError: if the files referened by `script` or `files` are not valid.
        """
        if self._slurm_id is not None:
            raise ValueError("a job is already submitted.  Use a new instance to run multiple jobs, or call release_job() to stop tracking slurm_id={}".format(self.slurm_id))

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
                _os.system(self.ssh_cmd+" \"echo {} > {}\"".format(self._slurm_id, _os.path.join(self.remote_directory, "crimpl_slurm_id")))

        return self._slurm_id

    def check_output(self, server_path, local_path="./",
                     wait_for_output=False):
        """
        Attempt to copy a file back from the server.

        Arguments
        -----------
        * `server_path` (string): path (relative to `directory`) on the server
            of the file to retrieve.
        * `local_path` (string, optional, default="./"): local path to copy
            the retrieved file.
        * `wait_for_output` (bool, optional, default=False): NOT IMPLEMENTED


        Returns
        ----------
        * None

        """
        if wait_for_output:
            raise NotImplementedError("wait_for_output not yet implemented")

        scp_cmd = self.scp_cmd_from.format(server_path=_os.path.join(self.remote_directory, server_path), local_path=local_path)
        # TODO: execute cmd, handle wait_for_output and also handle errors if stopped/terminated before getting results
        print("running: {}".format(scp_cmd))
        _os.system(scp_cmd)
