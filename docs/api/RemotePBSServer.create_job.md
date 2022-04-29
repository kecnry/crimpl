### [RemotePBSServer](RemotePBSServer.md).create_job (function)


```py

def create_job(self, job_name=None, conda_env=None, isolate_env=False, nprocs=4)

```



Create a child [RemotePBSJob](RemotePBSJob.md) instance.

Arguments
-----------
* `job_name` (string, optional, default=None): name for this job instance.
    If not provided, one will be created from the current datetime and
    accessible through [RemotePBSJob.job_name](RemotePBSJob.job_name.md).  This `job_name` will
    be necessary to reconnect to a previously submitted job.
* `conda_env` (string or None, optional, default=None): name of
    the conda environment to use for the job or False to not use a
    conda environment.  If not passed or None, will default to 'default'
    if conda is installed on the server or to False otherwise.
* `isolate_env` (bool, optional, default=False): whether to clone
    the `conda_env` for use in this job.  If True, any setup/installation
    done by this job will not affect the original environment and
    will not affect other jobs.  Note that the environment is cloned
    (and therefore isolated) at the first call to [RemotePBSServer.run_script](RemotePBSServer.run_script.md)
    or [RemotePBSServer.submit_script](RemotePBSServer.submit_script.md).  Setup in the parent environment can
    be done at the server level, but requires passing `conda_env`.
    Will raise an error if `isolate_env=True` and `conda_env=False`.
* `nnodes` (int, optional, default=1): default number of nodes to use
    when calling [RemotePBSJob.submit_job](RemotePBSJob.submit_job.md)
* `nprocs` (int, optional, default=4): default number of procs to use
    when calling [RemotePBSJob.submit_job](RemotePBSJob.submit_job.md)

Returns
---------
* [RemotePBSJob](RemotePBSJob.md)

