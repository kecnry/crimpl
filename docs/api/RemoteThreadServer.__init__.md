### [RemoteThreadServer](RemoteThreadServer.md).__init__ (function)


```py

def __init__(self, host, directory='~/crimpl', ssh='ssh', scp='scp', server_name=None)

```



Connect to a remote server running jobs in threads (no scheduler).

To create a new job, use [RemoteThreadServer.create_job](RemoteThreadServer.create_job.md) or to connect
to a previously created job, use [RemoteThreadServer.get_job](RemoteThreadServer.get_job.md).

Arguments
-----------
* `host` (string): host of the remote server.  Must be passwordless ssh-able.
    See [RemoteThreadServer.host](RemoteThreadServer.host.md)
* `directory` (string, optional, default='~/crimpl'): root directory of all
    jobs to run on the remote server.  The directory will be created
    if it does not already exist.
* `ssh` (string, optional, default='ssh'): command (and any arguments in
    addition to `host`) to ssh to the remote server.
* `scp` (string, optional, default='scp'): command (and any arguments)
    to copy files to the remote server.
* `server_name` (string): name to assign to the server.  If not provided,
    will be adopted automatically from `host` and available from
    [RemoteThreadServer.server_name](RemoteThreadServer.server_name.md).

