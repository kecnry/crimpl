### [AWSEC2Server](AWSEC2Server.md).create_job (function)


```py

def create_job(self, job_name=None, nprocs=4, InstanceType=None, ImageId='ami-03d315ad33b9d49c4', username='ubuntu', start=False)

```



Create a child &lt;AWSEC2Job&gt; instance.

Arguments
-----------
* `job_name` (string, optional, default=None): name for this job instance.
    If not provided, one will be created from the current datetime and
    accessible through &lt;AWSEC2Job.job_name&gt;.  This `job_name` will
    be necessary to reconnect to a previously submitted job.
* `nprocs` (int, optional, default=4): number of processors for the
    **job** EC2 instance.  The `InstanceType` will be determined and
    `nprocs` will be rounded up to the next available instance meeting
    those available requirements.
* `InstanceType` (string, optional, default=None):
* `ImageId` (string, optional, default='ami-03d315ad33b9d49c4'):
* `username` (string, optional, default='ubuntu'): username required
    to log in to the **job** EC2 instance.
* `start` (bool, optional, default=False): whether to immediately start
    the **job** EC2 instance.

Returns
----------
* &lt;AWSEC2Job&gt;

