### [RemoteSlurmServer](RemoteSlurmServer.md).__init__ (function)


```py

def __init__(self, host, directory=None)

```



Connect to a remote server running a Slurm scheduler.

To create a new job, use [RemoteSlurmScheduler.create_job](RemoteSlurmScheduler.create_job.md) or to connect
to a previously created job, use [RemoteSlurmScheduler.get_job](RemoteSlurmScheduler.get_job.md).

Arguments
-----------
* `host` (string): override host of the remote server.  Must be
    passwordless ssh-able.
* `directory` (string, optional, default=None): root directory of all
    jobs to run on the remote server.  The directory will be created
    if it does not already exist.

