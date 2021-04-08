from datetime import datetime as _datetime
import os as _os
import sys as _sys
import subprocess as _subprocess
from time import sleep as _sleep

__version__ = '0.1.0-dev2'

def _new_job_name():
    return _datetime.now().strftime('%Y.%m.%d-%H.%M.%S')

def _run_cmd(cmd):
    if cmd is None:
        return
    print("# crimpl: {}".format(cmd))
    return _subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

class Server(object):
    def __init__(self, directory=None):
        self._directory = directory
        self._directory_exists = False

    def __str__(self):
        return self.__repr__()

    @property
    def directory(self):
        return self._directory

    @property
    def _ssh_cmd(self):
        raise NotImplementedError("{} does not subclass _ssh_cmd".format(self.__class__.__name__))

    @property
    def ssh_cmd(self):
        """
        ssh command to the server

        Returns
        ----------
        * (string): command with "{}" placeholders for the command to run on the remote machine.
        """
        return "%s \'export PATH=\"%s/crimpl-bin:$PATH\"; {}\'" % (self._ssh_cmd, self.directory.replace("~", "$HOME"))

    def _run_ssh_cmd(self, cmd):
        ssh_cmd = self.ssh_cmd.format(cmd)
        # ssh_cmd = self.ssh_cmd+" \'export PATH=\"{directory}/crimpl-bin:$PATH\"; {cmd}\'".format(directory=self.directory.replace("~", "$HOME"), cmd=cmd)
        # ssh_cmd = self.ssh_cmd+" \'{cmd}\'".format(directory=self.directory.replace("~", "$HOME"), cmd=cmd)
        return _run_cmd(ssh_cmd)

    @property
    def scp_cmd_to(self):
        raise NotImplementedError("{} does not subclass scp_cmd_to".format(self.__class__.__name__))

    @property
    def scp_cmd_from(self):
        raise NotImplementedError("{} does not subclass scp_cmd_from".format(self.__class__.__name__))

    @property
    def existing_jobs(self):
        """
        """
        # TODO: override for EC2 to handle whatever servers are running (if the job server is running, have it check the status, otherwise have the server ec2 check the directory)

        try:
            out = self._run_ssh_cmd("ls -d {}/crimpl-job-*".format(self.directory))
        except _subprocess.CalledProcessError:
            return []

        directories = out.split()
        job_names = [d.split('crimpl-job-')[-1] for d in directories]
        return job_names

    @property
    def existing_jobs_status(self):
        """
        """
        # TODO: override for EC2 to handle whatever servers are running (if the job server is running, have it check the status, otherwise have the server ec2 check the directory)

        return {job_name: self.get_job(job_name).status for job_name in self.existing_jobs}

    @property
    def conda_installed(self):
        """
        Checks if conda is installed on the remote server

        See also:

        * <<class>.install_conda>

        Returns
        -----------
        * (bool)
        """
        try:
            out = self._run_ssh_cmd("conda -V")
        except _subprocess.CalledProcessError:
            return False
        return True

    def _get_conda_environments_dict(self, job_name=None):
        """

        Returns
        ---------
        * (dict)
        """
        out = self._run_ssh_cmd("conda info --envs")
        crimpl_env_dir = _os.path.join(self.directory, "crimpl-envs").replace("~", "")

        # force crimpl environments to override global
        d = {line.split()[0].split("/")[-1]: line.split()[-1] for line in out.split("\n")[3:] if len(line.split()) > 1}
        for line in out.split("\n")[3:]:
            if len(line.split()) == 1 and crimpl_env_dir in line:
                d[line.strip().split("/")[-1]] = line.strip()

        # force job clones environments to override crimpl/global
        if job_name is not None:
            for line in out.split("\n")[3:]:
                if len(line.split()) == 1 and "crimpl-job-{}".format(job_name) in line:
                    d[line.strip().split("/")[-1]] = line.strip()

        return d

    @property
    def conda_environments(self):
        """
        List (existing) available conda environments and their paths on the remote server.

        These will include those created at the root level (either within or outside crimpl)
        as well as those created by this <<class>> (which are stored in <<class>.directory>).
        In the case where the same name is available at the root level and created by
        this <<class>>, the one created by <<class>> will take precedence.

        Returns
        --------
        * (list)
        """
        return list(self._get_conda_environments_dict().keys())

    def _create_conda_environment(self, conda_environment,
                                  isolate_environment=False,
                                  job_name=None,
                                  check_if_exists=True,
                                  run_cmd=True):
        """
        """
        if not (isinstance(conda_environment, str) or conda_environment is None):
            raise TypeError("conda_environment must be a string or None")

        if isinstance(conda_environment, str) and "/" in conda_environment:
            raise ValueError("conda_environment should be alpha-numeric (and -/_) only")

        if conda_environment is None:
            conda_environment = 'default'

        python_version = _sys.version.split()[0]
        if isolate_environment and job_name is not None:
            # need to check to see if the server environment needs to be created and/or cloned
            conda_envs_dict = self._get_conda_environments_dict(job_name=job_name)

            cmd = ""
            envpath_server = _os.path.join(self.directory, "crimpl-envs", conda_environment)
            envpath = _os.path.join(self.directory, "crimpl-job-{}".format(job_name), "crimpl-envs", conda_environment)

            if conda_environment not in conda_envs_dict.keys():
                # create the environment at the server level
                cmd += "conda create -p {envpath_server} -y pip numpy python={python_version}; ".format(envpath_server=envpath_server, python_version=python_version)
            if len(cmd) or job_name not in conda_envs_dict.get(conda_environment):
                # clone the server environment at the job level
                cmd += "conda create -p {envpath} -y --clone {envpath_server};".format(envpath=envpath, envpath_server=envpath_server)

        else:
            if check_if_exists:
                conda_envs_dict = self._get_conda_environments_dict(job_name=job_name)
                if conda_environment in conda_envs_dict.keys():
                    return None, conda_envs_dict.get(conda_environment)
            else:
                conda_envs_dict = False

            # create the environment at the server level
            envpath = _os.path.join(self.directory, "crimpl-envs", conda_environment)
            cmd = "conda create -p {envpath} -y pip numpy python={python_version}".format(envpath=envpath, python_version=python_version)

        if run_cmd:
            return self._run_ssh_cmd(cmd), envpath
        else:
            return self.ssh_cmd.format(cmd), envpath


    def _create_crimpl_directory(self):

        if self._directory_exists:
            return True

        try:
            out = self._run_ssh_cmd("mkdir -p {directory}".format(directory=self.directory))
        except _subprocess.CalledProcessError:
            return False
        self._directory_exists = True
        return True


    def install_conda(self):
        """
        Install conda on the remote server if it is not already installed.

        See also:

        * <<class>.conda_installed>
        """
        if self.conda_installed:
            return

        self._create_crimpl_directory()

        # out = self._run_ssh_cmd("cd {directory}; wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh; sh Miniconda3-latest-Linux-x86_64.sh -u -b -p ./crimpl-conda; mkdir ./crimpl-bin; cp ./crimpl-conda/bin/conda ./crimpl-bin/conda; conda init".format(directory=self.directory))
        out = self._run_ssh_cmd("cd {directory}; wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh; sh Miniconda3-latest-Linux-x86_64.sh -u -b -p ./crimpl-conda; ./crimpl-conda/bin/conda init".format(directory=self.directory))

        return self.conda_installed

    def _submit_script_cmds(self, script, files,
                            use_slurm,
                            directory,
                            conda_environment, isolate_environment,
                            job_name,
                            terminate_on_complete=False,
                            use_screen=False,
                            **slurm_kwargs):
        # from job: self.server._submit_script_cmds(script, files, use_slurm, directory=self.remote_directory, conda_environment=self.conda_environment, isolate_environment=self.isolate_environment, job_name=self.job_name)
        # from server: self._submit_script_cmds(script, files, use_slurm=False, directory=self.directory, conda_environment=conda_environment, isolate_environment=False, job_name=None)

        if isinstance(script, str):
            # TODO: allow for http?
            if not _os.path.isfile(script):
                raise ValueError("cannot find valid script at {}.  To pass commands directly, pass a list of strings".format(script))

            f = open(script, 'r')
            script = script.readlines()

        if not isinstance(script, list):
            raise TypeError("script must be of type string (path) or list (list of commands)")

        # for i, line in enumerate(script):
        #     # ensure that all calls to conda install without prompts?
        #     if "conda" in line and "-y" not in line:
        #         script[i] = script[i] + " -y"

        _slurm_kwarg_to_prefix = {'job_name': '-J ',
                                  'nprocs': '-n ',
                                  'walltime': '-t ',
                                  'mail_type': '--mail-type=',
                                  'mail_user': '--mail-user='}

        create_env_cmd, conda_env_path = self._create_conda_environment(conda_environment, isolate_environment, job_name=job_name, check_if_exists=True, run_cmd=False)

        if use_slurm and job_name is None:
            raise ValueError("use_slurm requires job_name")
        if use_slurm and use_screen:
            raise ValueError("cannot use both use_slurm and use_screen")

        if job_name is not None:
            if use_slurm:
                slurm_script = ["#!/bin/bash"]
                # TODO: use job subdirectory
                slurm_script += ["#SBATCH -D {}".format(directory+"/")]
                for k,v in slurm_kwargs.items():
                    prefix = _slurm_kwarg_to_prefix.get(k, False)
                    if prefix is False:
                        raise NotImplementedError("slurm command for {} not implemented".format(k))
                    slurm_script += ["#SBATCH {}{}".format(prefix, v)]

                script = slurm_script + ["\n\n", "eval \"$(conda shell.bash hook)\"", "conda activate {}".format(conda_env_path)] + ["echo \'running\' > crimpl-job.status"] + script + ["echo \'complete\' > crimpl-job.status"]
            else:
                # need to track status by writing to log file
                if "#!" in script[0]:
                    script = [script[0]] + ["echo \'running\' > crimpl-job.status"] + script[1:] + ["echo \'complete\' > crimpl-job.status"]
                else:
                    script = ["echo \'running\' > crimpl-job.status"] + script + ["echo \'complete\' > crimpl-job.status"]


        # TODO: use tmp file instead
        f = open('crimpl_script.sh', 'w')
        if not use_slurm:
            f.write("eval \"$(conda shell.bash hook)\"\nconda activate {}\n".format(conda_env_path))
        f.write("\n".join(script))
        if terminate_on_complete:
            # should really only be used for AWS
            f.write("\nsudo shutdown now")
        f.close()

        if not isinstance(files, list):
            raise TypeError("files must be of type list")
        for f in files:
            if not _os.path.isfile(f):
                raise ValueError("cannot find file at {}".format(f))

        mkdir_cmd = self.ssh_cmd.format("mkdir -p {}".format(directory))
        if job_name is not None:
            logfiles_cmd = self.ssh_cmd.format("echo \'{}\' >> {}".format(" ".join([_os.path.basename(f) for f in files]), _os.path.join(directory, "crimpl-input-files.list"))) if len(files) else None
            logenv_cmd = self.ssh_cmd.format("echo \'{}\' > {}".format(conda_environment, _os.path.join(directory, "crimpl-conda-environment")))

        # TODO: use job subdirectory for server_path
        scp_cmd = self.scp_cmd_to.format(local_path=" ".join(["crimpl_script.sh"]+files), server_path=directory+"/")

        if use_slurm:
            remote_script = _os.path.join(directory, _os.path.basename("crimpl_script.sh"))
            cmd = self.ssh_cmd.format("sbatch {remote_script}".format(remote_script=remote_script))
        else:
            remote_script = "crimpl_script.sh"
            cmd = self.ssh_cmd.format("cd {directory}; chmod +x {remote_script}; {screen} sh {remote_script}".format(directory=directory,
                                                                                                                     remote_script=remote_script,
                                                                                                                     screen="screen -m -d " if use_screen else ""))
        if job_name is not None:
            return [mkdir_cmd, scp_cmd, logfiles_cmd, logenv_cmd, create_env_cmd, cmd]
        else:
            return [mkdir_cmd, scp_cmd, create_env_cmd, cmd]

    def create_job(self, job_name=None, conda_environment=None, isolate_environment=False):
        """
        """
        return self._JobClass(server=self,
                              job_name=job_name,
                              conda_environment=conda_environment,
                              isolate_environment=isolate_environment,
                              connect_to_existing=False)

    def get_job(self, job_name=None):
        """
        """
        return self._JobClass(server=self, job_name=job_name, connect_to_existing=True)

    def submit_job(self, job_name=None, conda_environment=None, isolate_environment=False,
                   **submit_script_kwargs):
        """
        Shortcut to <<class>.create_job> followed by the relevant `submit_script`


        """
        sj = self.create_job(job_name=job_name, conda_environment=conda_environment, isolate_environment=isolate_environment)
        return sj.submit_script(**submit_script_kwargs)

class ServerJob(object):
    def __init__(self, server, job_name=None,
                 conda_environment=None, isolate_environment=False,
                 job_submitted=False):
        self._server = server

        self._job_name = job_name
        self._job_submitted = job_submitted


        if not (isinstance(conda_environment, str) or conda_environment is None):
            raise TypeError("conda_environment must be a string or None")
        if isinstance(conda_environment, str) and "/" in conda_environment:
            raise ValueError("conda_environment should be alpha-numeric (and -/_) only")
        self._conda_environment = conda_environment

        if not isinstance(isolate_environment, bool):
            raise TypeError("isolate_environment must be of type bool")
        self._isolate_environment = isolate_environment

        # allow caching once the environment exists
        self._conda_environment_exists = False

        # allow for caching remote_directory
        self._remote_directory = None

        # allow caching for input files
        self._input_files = None

    def __str__(self):
        return self.__repr__()

    @property
    def server(self):
        """
        Access the parent server object
        """
        return self._server

    @property
    def conda_environment(self):
        """
        Name of the conda environment to use for any future calls
        to <<class>.run_script> or <<class>.submit_script>.

        If the environment does not exist, it will be created during the next
        call to <<class>.run_script> or <<class>.submit_script>.

        See also:

        * <class>.conda_environment_exists>
        * <Server.conda_environments>

        Returns
        -----------
        * (str): name or path of the conda environment on the remote server.
        """
        if self._conda_environment is None:
            # determine if already stored in the remote directory
            try:
                response = self.server._run_ssh_cmd("cat {}".format(_os.path.join(self.remote_directory, "crimpl-conda-environment")))
            except _subprocess.CalledProcessError as e:
                if 'No such file or directory' in str(e):
                    # then the cached file does not yet exist, so we'll default to 'default'
                    self._conda_environment = 'default'
                    print("# crimpl: will use conda_environment=\"default\"")
                else:
                    # leave self._conda_environment at None
                    pass
            else:
                self._conda_environment = response.strip()

        return self._conda_environment

    @property
    def isolate_environment(self):
        """
        """
        return self._isolate_environment

    @property
    def conda_environment_exists(self):
        """
        Check whether <<class>.conda_environment> exists on the remote machine.

        Returns
        ----------
        * (bool)
        """
        if not self._conda_environment_exists:
            self._conda_environment_exists = self.conda_environment in self.server.conda_environments
        return self._conda_environment_exists

    def create_conda_environment(self):
        """
        Create a conda environment (in the <<Server>.remote_directory>) named
        <<class>.conda_environment>.

        This environment will be available to any jobs in this server and will
        be listed in <<Server>.conda_environments>.  The created environment will
        use the same version of python as the local version and include both
        pip and numpy, by default.

        """
        if self.conda_environment_exists:
            return

        return self.server._create_conda_environment(conda_environment, check_if_exists=False)

    @property
    def job_name(self):
        """
        Access the job name

        Returns
        ----------
        * (string)
        """
        return self._job_name

    @property
    def remote_directory(self):
        """
        Access the **job** subdirectory location on the remote server.

        Returns
        ----------
        * (string)
        """
        if self._remote_directory is None:
            # NOTE: for AWSEC2 self.server.ssh_cmd may point to the job EC2 instance if the server is not running
            home_dir = self.server._run_ssh_cmd("pwd")
            if "~" in self.server.directory:
                self._remote_directory = _os.path.join(self.server.directory.replace("~", home_dir), "crimpl-job-{}".format(self.job_name))
            else:
                self._remote_directory = _os.path.join(home_dir, self.server.directory, "crimpl-job-{}".format(self.job_name))
        return self._remote_directory

    @property
    def ls(self):
        """
        List all files in the **job** subdirectory on the remote server.

        See also:

        * <<class>.job_files>
        * <<class>.input_files>
        * <<class>.output_files>

        Returns
        ----------
        * (list)
        """
        response = self.server._run_ssh_cmd("ls {}/*".format(self.remote_directory))
        return [_os.path.basename(f) for f in response.split()]

    @property
    def job_files(self):
        """
        List the files in the **job** subdirectory on the remote server, including
        files sent to the server and output files, but excluding files created
        and managed by **crimpl**.

        See also:

        * <<class>.ls>
        * <<class>.input_files>
        * <<class>.output_files>

        Returns
        -------------
        * (list)
        """
        return [f for f in self.ls if f[:6]!='crimpl']

    @property
    def input_files(self):
        """
        List the **input** files in the **job** subdirectory on the remote server.

        These were files sent via <<class>.submit_job>.

        See also:

        * <<class>.ls>
        * <<class>.job_files>
        * <<class>.output_files>

        Returns
        -----------
        * (list)
        """
        if self._input_files is None:

            response = self.server._run_ssh_cmd("cat {}".format(_os.path.join(self.remote_directory, "crimpl-input-files.list")))
            self._input_files = response.split()

        return self._input_files

    @property
    def output_files(self):
        """
        List the **output** files in the **job** subdirectory on the remote server.

        These are all <<class>.job_files> that are not included in <<class>.input_files>.

        See also:

        * <<class>.ls>
        * <<class>.job_files>
        * <<class>.input_files>

        Returns
        ----------
        * (list)
        """
        return [f for f in self.job_files if f not in self.input_files]

    def wait_for_job_status(self, status='complete',
                            error_if=['failed', 'canceled'],
                            sleeptime=5):
        """
        Wait for the job to reach a desired job_status.

        Arguments
        -----------
        * `status` (string or list, optional, default='complete'): status
            or statuses to exit the wait loop successfully.
        * `error_if` (string or list, optional, default=['failed', 'canceled']): status or
            statuses to exit the wait loop and raise an error.
        * `sleeptime` (int, optional, default=5): number of seconds to wait
            between successive job status checks.

        Returns
        ----------
        * (string): `status`
        """
        if status is True:
            status = 'complete'

        if isinstance(status, str):
            status = [status]

        if isinstance(error_if, str):
            error_if = [error_if]

        while True:
            job_status = self.job_status
            print("# crimpl: job_status={}".format(job_status))
            if job_status in status:
                break
            if job_status in error_if:
                raise ValueError("job_status={}".format(job_status))
            _sleep(sleeptime)

        return job_status

    def check_output(self, server_path=None, local_path="./"):
        """
        Attempt to copy a file(s) back from the remote server.

        Arguments
        -----------
        * `server_path` (string or list or None, optional, default=None): path(s)
            (relative to `directory`) on the server of the file(s) to retrieve.
            If not provided or None, will default to <<class>.output_files>.
            See also: <<class>.ls> or <<class>.job_files> for a full list of
            available files on the remote server.
        * `local_path` (string, optional, default="./"): local path to copy
            the retrieved file.


        Returns
        ----------
        * None
        """


        if server_path is None:
            server_path = self.output_files

        if isinstance(server_path, str):
            server_path_str = _os.path.join(self.remote_directory, server_path)
        else:
            server_path_str = "%s/{%s}" %  (self.remote_directory, ",".join(server_path))

        scp_cmd = self.server.scp_cmd_from.format(server_path=server_path_str, local_path=local_path)
        # TODO: execute cmd, and handle errors if stopped/terminated before getting results
        _run_cmd(scp_cmd)
