### [LocalThreadServer](LocalThreadServer.md).__init__ (function)


```py

def __init__(self, directory='~/crimpl', server_name=None)

```



Run scripts and jobs in threads in an isolated directory on the local machine.

To create a new job, use [LocalThreadServer.create_job](LocalThreadServer.create_job.md) or to connect
to a previously created job, use [LocalThreadServer.get_job](LocalThreadServer.get_job.md).

Arguments
-----------
* `directory` (string, optional, default='~/crimpl'): root directory of all
    jobs to run in the server directory.  The directory will be created
    if it does not already exist.
* `server_name` (string): name to assign to the server.  If not provided,
    will be adopted automatically from `host` and available from
    [LocalThreadServer.server_name](LocalThreadServer.server_name.md).

