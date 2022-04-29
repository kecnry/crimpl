### [RemotePBSJob](RemotePBSJob.md).__init__ (function)


```py

def __init__(self, server=None, job_name=None, conda_env=None, isolate_env=False, nprocs=4, slurm_id=None, connect_to_existing=None)

```



Create and submit a job on a [RemotePBSServer](RemotePBSServer.md).

Under-the-hood, this creates a subdirectory in [RemotePBSServer.directory](RemotePBSServer.directory.md)
based on the provided or assigned `job_name`.  All submitted scripts/files
(through either [RemotePBSJob.run_script](RemotePBSJob.run_script.md) or [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md))
are copied to and run in this directory.

Arguments
-------------
* `server` ([RemotePBSServer](RemotePBSServer.md), optional, default=None): server to
    use when running the job.  If `server` is not provided, `host` must
    be provided.
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
    (and therefore isolated) at the first call to [RemotePBSJob.run_script](RemotePBSJob.run_script.md)
    or [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md).  Setup in the parent environment can
    be done at the server level, but requires passing `conda_env`.
    Will raise an error if `isolate_env=True` and `conda_env=False`.
* `nnodes` (int, optional, default=1): default number of nodes to use
    when calling [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md)
* `nprocs` (int, optional, default=4): default number of procs to use
    when calling [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md)
* `pbs_id` (int, optional, default=None): internal id of the remote
    PBS job.  If unknown, this will be determined automatically.
    Do **NOT** set `pbs_id` for a new [RemotePBSJob](RemotePBSJob.md) instance.
* `connect_to_existing` (bool, optional, default=None): NOT YET IMPLEMENTED

