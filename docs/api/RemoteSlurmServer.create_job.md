### [RemoteSlurmServer](RemoteSlurmServer.md).create_job (function)


```py

def create_job(self, job_name=None, conda_environment=None, isolate_environment=False, nprocs=4)

```



Create a child [RemoteSlurmJob](RemoteSlurmJob.md) instance.

Arguments
-----------
* `job_name` (string, optional, default=None): name for this job instance.
    If not provided, one will be created from the current datetime and
    accessible through [RemoteSlurmJob.job_name](RemoteSlurmJob.job_name.md).  This `job_name` will
    be necessary to reconnect to a previously submitted job.
* `conda_environment` (string or None, optional, default=None): name of
    the conda environment to use for the job, or None to use the
    'default' environment stored in the server crimpl directory.
* `isolate_environment` (bool, optional, default=False): whether to clone
    the `conda_environment` for use in this job.  If True, any setup/installation
    done by this job will not affect the original environment and
    will not affect other jobs.  Note that the environment is cloned
    (and therefore isolated) at the first call to [RemoteSlurmServer.run_script](RemoteSlurmServer.run_script.md)
    or [RemoteSlurmServer.submit_script](RemoteSlurmServer.submit_script.md).  Setup in the parent environment can
    be done at the server level, but requires passing `conda_environment`.
* `nprocs` (int, optional, default=4): default number of procs to use
    when calling [RemoteSlurmJob.submit_job](RemoteSlurmJob.submit_job.md)

Returns
---------
* [RemoteSlurmJob](RemoteSlurmJob.md)

