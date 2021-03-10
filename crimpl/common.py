from datetime import datetime as _datetime
import os as _os
import subprocess as _subprocess

__version__ = '0.1.0-dev1'

def _new_job_name():
    return _datetime.now().strftime('%Y.%d.%m-%H.%M.%S')

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
    def __init__(self, server, job_name=None):
        self._server = server

        self._job_name = job_name

        # allow for caching remote_directory
        self._remote_directory = None

    def __str__(self):
        return self.__repr__()

    @property
    def server(self):
        return self._server

    @property
    def job_name(self):
        """
        """
        return self._job_name

    @property
    def remote_directory(self):
        """
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
