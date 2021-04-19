### [AWSEC2Server](AWSEC2Server.md).create_job (function)


```py

def create_job(self, job_name=None, conda_env=None, isolate_env=False, nprocs=4, InstanceType=None, ImageId='ami-03d315ad33b9d49c4', username='ubuntu', start=False)

```



Create a child &lt;AWSEC2Job&gt; instance.

Arguments
-----------
* `job_name` (string, optional, default=None): name for this job instance.
    If not provided, one will be created from the current datetime and
    accessible through &lt;AWSEC2Job.job_name&gt;.  This `job_name` will
    be necessary to reconnect to a previously submitted job.
* `conda_env` (string or None, optional, default=None): name of
    the conda environment to use for the job, or None to use the
    'default' environment stored in the server crimpl directory.
* `isolate_env` (bool, optional, default=False): whether to clone
    the `conda_env` for use in this job.  If True, any setup/installation
    done by this job will not affect the original environment and
    will not affect other jobs.  Note that the environment is cloned
    (and therefore isolated) at the first call to &lt;AWSEC2Server.run_script&gt;
    or &lt;AWSEC2Server.submit_script&gt;.  Setup in the parent environment can
    be done at the server level, but requires passing `conda_env`.
* `nprocs` (int, optional, default=4): number of processors for the
    **job** EC2 instance.  The `InstanceType` will be determined and
    `nprocs` will be rounded up to the next available instance meeting
    those available requirements.
* `InstanceType` (string, optional, default=None):
* `ImageId` (string, optional, default=None):  ImageId of the **job**
    EC2 instance.  If None or not provided, will default to the same
    as the **server** EC2 instance (Ubuntu 20.04).
* `username` (string, optional, default='ubuntu'): username required
    to log in to the **job** EC2 instance.  If None or not provided,
    will default to &lt;AWSEC2Server.username&gt;.
* `start` (bool, optional, default=False): whether to immediately start
    the **job** EC2 instance.

Returns
----------
* &lt;AWSEC2Job&gt;

