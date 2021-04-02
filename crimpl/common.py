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

    def _get_conda_environments_dict(self):
        """

        Returns
        ---------
        * (dict)
        """
        out = self._run_ssh_cmd("conda info --envs")
        crimpl_env_dir = _os.path.join(self.directory, "crimpl-envs").replace("~", "")

        # force local to override global
        d = {line.split()[0].split("/")[-1]: line.split()[-1] for line in out.split("\n")[3:] if len(line.split()) > 1}
        for line in out.split("\n")[3:]:
            if len(line.split()) == 1 and crimpl_env_dir in line:
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

    def _create_conda_environment(self, conda_environment, check_if_exists=True, run_cmd=True):
        """
        """
        if not (isinstance(conda_environment, str) or conda_environment is None):
            raise TypeError("conda_environment must be a string or None")

        if isinstance(conda_environment, str) and "/" in conda_environment:
            raise ValueError("conda_environment should be alpha-numeric (and -/_) only")

        if conda_environment is None:
            conda_environment = 'default'

        if check_if_exists:
            conda_envs_dict = self._get_conda_environments_dict()
            if conda_environment in conda_envs_dict.keys():
                return None, conda_envs_dict.get(conda_environment)

        envpath = _os.path.join(self.directory, "crimpl-envs", conda_environment)
        python_version = _sys.version.split()[0]

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

    def create_job(self, job_name=None, conda_environment=None):
        """
        """
        return self._JobClass(server=self,
                              job_name=job_name,
                              conda_environment=conda_environment,
                              connect_to_existing=False)

    def get_job(self, job_name=None):
        """
        """
        return self._JobClass(server=self, job_name=job_name, connect_to_existing=True)

class ServerJob(object):
    def __init__(self, server, job_name=None, conda_environment=None, job_submitted=False):
        self._server = server

        self._job_name = job_name
        self._job_submitted = job_submitted

        self.conda_environment = conda_environment

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
            return 'default'

        return self._conda_environment

    @conda_environment.setter
    def conda_environment(self, conda_environment):
        """
        Set the conda environment to use for any future calls to <<class>.run_script>
        or <<class>.submit_script>.

        Arguments
        ------------
        * `conda_environment` (string or None): name of the conda environment, or
            None to use the 'default' environment stored in the server crimpl directory.
        """
        # TODO: only allow changing before submission

        # make sure a valid string


        if not (isinstance(conda_environment, str) or conda_environment is None):
            raise TypeError("conda_environment must be a string or None")

        if isinstance(conda_environment, str) and "/" in conda_environment:
            raise ValueError("conda_environment should be alpha-numeric (and -/_) only")

        self._conda_environment = conda_environment

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
        response = self._run_ssh_cmd("ls {}/*".format(self.remote_directory))
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

            response = self._run_ssh_cmd("cat {}".format(_os.path.join(self.remote_directory, "crimpl-input-files.list")))
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
            if job_status in status:
                break
            if job_status in error_if:
                raise ValueError("job_status={}".format(job_status))
            _sleep(sleeptime)

        return status

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
