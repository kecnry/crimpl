### [AWSEC2Job](AWSEC2Job.md).__init__ (function)


```py

def __init__(self, server, job_name=None, connect_to_existing=None, nprocs=None, InstanceType=None, ImageId='ami-03d315ad33b9d49c4', username='ubuntu', start=False)

```



Arguments
-------------
* `server`
* `job_name` (string, optional, default=None): name for this job instance.
    If not provided, one will be created from the current datetime and
    accessible through [RemoteSlurmJob.job_name](RemoteSlurmJob.job_name.md).  This `job_name` will
    be necessary to reconnect to a previously submitted job.
* `connect_to_existing` (bool, optional, default=None): NOT YET IMPLEMENTED
* `nprocs`
* `InstanceType`
* `ImageId`
* `username`
* `start`

