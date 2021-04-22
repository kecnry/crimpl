### [LocalThreadJob](LocalThreadJob.md).__init__ (function)


```py

def __init__(self, server=None, job_name=None, conda_env=None, isolate_env=False, connect_to_existing=None)

```



Create and submit a job on a [LocalThreadServer](LocalThreadServer.md).

Under-the-hood, this creates a subdirectory in [LocalThreadServer.directory](LocalThreadServer.directory.md)
based on the provided or assigned `job_name`.  All submitted scripts/files
(through either [LocalThreadJob.run_script](LocalThreadJob.run_script.md) or [LocalThreadJob.submit_script](LocalThreadJob.submit_script.md))
are copied to and run in this directory.

Arguments
-------------
* `server` ([LocalThreadServer](LocalThreadServer.md), optional, default=None): server to
    use when running the job.
* `job_name` (string, optional, default=None): name for this job instance.
    If not provided, one will be created from the current datetime and
    accessible through [LocalThreadJob.job_name](LocalThreadJob.job_name.md).  This `job_name` will
    be necessary to reconnect to a previously submitted job.
* `conda_env` (string or None, optional, default=None): name of
    the conda environment to use for the job or False to not use a
    conda environment.  If not passed or None, will default to 'default'
    if conda is installed on the server or to False otherwise.
* `isolate_env` (bool, optional, default=False): whether to clone
    the `conda_env` for use in this job.  If True, any setup/installation
    done by this job will not affect the original environment and
    will not affect other jobs.  Note that the environment is cloned
    (and therefore isolated) at the first call to [LocalThreadJob.run_script](LocalThreadJob.run_script.md)
    or [LocalThreadJob.submit_script](LocalThreadJob.submit_script.md).  Setup in the parent environment can
    be done at the server level, but requires passing `conda_env`.
    Will raise an error if `isolate_env=True` and `conda_env=False`.
* `connect_to_existing` (bool, optional, default=None): NOT YET IMPLEMENTED

