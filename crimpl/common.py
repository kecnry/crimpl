from datetime import datetime as _datetime
import os as _os
import subprocess as _subprocess
from time import sleep as _sleep

__version__ = '0.1.0-dev1'

def _new_job_name():
    return _datetime.now().strftime('%Y.%m.%d-%H.%M.%S')

class Server(object):
    def __init__(self, directory=None):
        self._directory = directory

    def __str__(self):
        return self.__repr__()

    @property
    def directory(self):
        return self._directory

    @property
    def ssh_cmd(self):
        raise NotImplementedError("{} does not subclass ssh_cmd".format(self.__class__.__name__))

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
            out = _subprocess.check_output(self.ssh_cmd+" \"ls -d {}/crimpl-job-*\"".format(self.directory), shell=True).decode('utf-8').strip()
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

    def create_job(self, job_name=None):
        """
        """
        return self._JobClass(server=self, job_name=job_name, connect_to_existing=False)

    def get_job(self, job_name=None):
        """
        """
        return self._JobClass(server=self, job_name=job_name, connect_to_existing=True)

class ServerJob(object):
    def __init__(self, server, job_name=None, job_submitted=False):
        self._server = server

        self._job_name = job_name
        self._job_submitted = job_submitted

        # allow for caching remote_directory
        self._remote_directory = None

    def __str__(self):
        return self.__repr__()

    @property
    def server(self):
        """
        Access the parent server object
        """
        return self._server

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
            if self.__class__.__name__ == 'AWSEC2Job':
                if self._instanceId is not None:
                    ssh_cmd = self.ssh_cmd
                else:
                    ssh_cmd = self.server.ssh_cmd
            else:
                ssh_cmd = self.server.ssh_cmd
            home_dir = _subprocess.check_output(ssh_cmd+" \"pwd\"", shell=True).decode('utf-8').strip()
            if "~" in self.server.directory:
                self._remote_directory = _os.path.join(self.server.directory.replace("~", home_dir), "crimpl-job-{}".format(self.job_name))
            else:
                self._remote_directory = _os.path.join(home_dir, self.server.directory, "crimpl-job-{}".format(self.job_name))
        return self._remote_directory

    def wait_for_job_status(self, status='complete', sleeptime=5):
        """
        Wait for the job to reach a desired job_status.

        Arguments
        -----------
        * `status` (string or list, optional, default='complete'): status
            or statuses to exit the wait loop.
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

        while self.job_status not in status:
            _sleep(sleeptime)
        return self.job_status
