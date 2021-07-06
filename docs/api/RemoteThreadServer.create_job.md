### [RemoteThreadServer](RemoteThreadServer.md).create_job (function)


```py

def create_job(self, job_name=None, conda_env=None, isolate_env=False)

```



Create a child [RemoteThreadJob](RemoteThreadJob.md) instance.

Arguments
-----------
* `job_name` (string, optional, default=None): name for this job instance.
    If not provided, one will be created from the current datetime and
    accessible through [RemoteThreadJob.job_name](RemoteThreadJob.job_name.md).  This `job_name` will
    be necessary to reconnect to a previously submitted job.
* `conda_env` (string or None, optional, default=None): name of
    the conda environment to use for the job or False to not use a
    conda environment.  If not passed or None, will default to 'default'
    if conda is installed on the server or to False otherwise.
* `isolate_env` (bool, optional, default=False): whether to clone
    the `conda_env` for use in this job.  If True, any setup/installation
    done by this job will not affect the original environment and
    will not affect other jobs.  Note that the environment is cloned
    (and therefore isolated) at the first call to [RemoteThreadServer.run_script](RemoteThreadServer.run_script.md)
    or [RemoteThreadServer.submit_script](RemoteThreadServer.submit_script.md).  Setup in the parent environment can
    be done at the server level, but requires passing `conda_env`.
    Will raise an error if `isolate_env=True` and `conda_env=False`.


Returns
---------
* [RemoteThreadJob](RemoteThreadJob.md)

