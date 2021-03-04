from datetime import datetime as _datetime
import os as _os
import subprocess as _subprocess

class Server(object):
    def __init__(self, config, directory=None):
        self._config = config

        if directory is not None:
            # TODO: make a deepcopy of config first to avoid editing to user copy?
            self.config.directory = directory

    def __str__(self):
        return self.__repr__()

    @property
    def config(self):
        """
        """
        # should subclass just to override API docs
        return self._config

    @property
    def directory(self):
        return self.config.directory

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
        out = _subprocess.check_output(self.ssh_cmd+" \"ls -d {}/crimpl-*\"".format(self.directory), shell=True).decode('utf-8').strip()
        directories = out.split()
        job_names = [d.split('crimpl-')[-1] for d in directories]
        return job_names

    @property
    def existing_jobs_status(self):
        """
        """
        return {job_name: self.get_job(job_name).status for job_name in self.existing_jobs}

    def create_job(self, job_name=None):
        """
        """
        return self._JobClass(server=self, job_name=job_name)#, connect_to_existing=False)

    def get_job(self, job_name=None):
        """
        """
        return self._JobClass(server=self, job_name=job_name)#, connect_to_existing=True)

class ServerJob(object):
    def __init__(self, server, job_name=None, directory=None, connect_to_existing=None):
        self._server = server

        if connect_to_existing is None:
            if job_name is None:
                job_name = _datetime.now().strftime('%Y.%d.%m-%H.%M.%S')
            # otherwise we'll connect to an existing if it matches, or create a new one
        elif connect_to_existing:
            if job_name is None:
                # TODO: look in self.config.remote_directory, if a SINGLE
                # job subdirectory exists, then adopt that job_name,
                # if more than 1 exist: raise an error.
                raise NotImplementedError("connect_to_existing not yet supported")
            else:
                # TODO: make sure that job_name exists on the remote sever or raise error
                raise NotImplementedError("connect_to_existing not yet supported")
        else:
            if job_name is None:
                job_name = _datetime.now().strftime('%Y.%d.%m-%H.%M.%S')
            else:
                # TODO: make sure that job_name DOES NOT exist on the remote server or raise error
                raise NotImplementedError("connect_to_existing=False not yet supported")

        self._job_name = job_name

        if directory is not None:
            # TODO: make a deepcopy of config first to avoid editing to user copy?
            self.server.config.directory = directory

        # allow for caching remote_directory
        self._remote_directory = None

    def __str__(self):
        return self.__repr__()

    @property
    def server(self):
        return self._server

    @property
    def config(self):
        return self.server.config

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
            home_dir = _subprocess.check_output(self.server.ssh_cmd+" \"pwd\"", shell=True).decode('utf-8').strip()
            if "~" in self.config.directory:
                self._remote_directory = _os.path.join(self.config.directory.replace("~", home_dir), "crimpl-{}".format(self.job_name))
            else:
                self._remote_directory = _os.path.join(home_dir, self.config.directory, "crimpl-{}".format(self.job_name))
        return self._remote_directory
