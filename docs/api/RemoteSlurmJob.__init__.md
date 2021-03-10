### [RemoteSlurmJob](RemoteSlurmJob.md).__init__ (function)


```py

def __init__(self, server=None, job_name=None, slurm_id=None, connect_to_existing=None)

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
* `slurm_id` (int, optional, default=None): internal id of the remote
    slurm job.  If unknown, this will be determined automatically.
    Do **NOT** set `slurm_id` for a new [RemoteSlurmJob](RemoteSlurmJob.md) instance.
* `connect_to_existing` (bool, optional, default=None): NOT YET IMPLEMENTED

