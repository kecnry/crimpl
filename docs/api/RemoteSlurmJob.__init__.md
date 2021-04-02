### [RemoteSlurmJob](RemoteSlurmJob.md).__init__ (function)


```py

def __init__(self, server=None, job_name=None, conda_environment=None, isolate_environment=False, nprocs=4, slurm_id=None, connect_to_existing=None)

```



Create and submit a job on a [RemoteSlurmServer](RemoteSlurmServer.md).

Under-the-hood, this creates a subdirectory in [RemoteSlurmServer.directory](RemoteSlurmServer.directory.md)
based on the provided or assigned `job_name`.  All submitted scripts/files
(through either [RemoteSlurmJob.run_script](RemoteSlurmJob.run_script.md) or [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md))
are copied to and run in this directory.

Arguments
-------------
* `server` ([RemoteSlurmServer](RemoteSlurmServer.md), optional, default=None): server to
    use when running the job.  If `server` is not provided, `host` must
    be provided.
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
    (and therefore isolated) at the first call to [RemoteSlurmJob.run_script](RemoteSlurmJob.run_script.md)
    or [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md).  Setup in the parent environment can
    be done at the server level, but requires passing `conda_environment`.
* `nprocs` (int, optional, default=4): default number of procs to use
    when calling [RemoteSlurmJob.submit_job](RemoteSlurmJob.submit_job.md)
* `slurm_id` (int, optional, default=None): internal id of the remote
    slurm job.  If unknown, this will be determined automatically.
    Do **NOT** set `slurm_id` for a new [RemoteSlurmJob](RemoteSlurmJob.md) instance.
* `connect_to_existing` (bool, optional, default=None): NOT YET IMPLEMENTED

