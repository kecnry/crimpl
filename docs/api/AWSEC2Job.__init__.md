### [AWSEC2Job](AWSEC2Job.md).__init__ (function)


```py

def __init__(self, server, job_name=None, conda_environment=None, isolate_environment=False, connect_to_existing=None, nprocs=None, InstanceType=None, ImageId='ami-03d315ad33b9d49c4', username='ubuntu', start=False)

```



Arguments
-------------
* `server`
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
    (and therefore isolated) at the first call to &lt;AWSEC2Job.run_script&gt;
    or &lt;AWSEC2Job.submit_script&gt;.  Setup in the parent environment can
    be done at the server level, but requires passing `conda_environment`.
* `connect_to_existing` (bool, optional, default=None): NOT YET IMPLEMENTED
* `nprocs`
* `InstanceType`
* `ImageId`
* `username`
* `start`

