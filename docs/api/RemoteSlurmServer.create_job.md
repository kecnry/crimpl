### [RemoteSlurmServer](RemoteSlurmServer.md).create_job (function)


```py

def create_job(self, job_name=None, conda_environment=None, nprocs=4)

```



Create a child [RemoteSlurmJob](RemoteSlurmJob.md) instance.

Arguments
-----------
* `job_name` (string, optional, default=None): name for this job instance.
    If not provided, one will be created from the current datetime and
    accessible through [RemoteSlurmJob.job_name](RemoteSlurmJob.job_name.md).  This `job_name` will
    be necessary to reconnect to a previously submitted job.
* `conda_environment` (string or None): name of the conda environment to
    use for the job, or None to use the 'default' environment stored in
    the server crimpl directory.
* `nprocs` (int, optional, default=4): default number of procs to use
    when calling [RemoteSlurmJob.submit_job](RemoteSlurmJob.submit_job.md)

Returns
---------
* [RemoteSlurmJob](RemoteSlurmJob.md)

