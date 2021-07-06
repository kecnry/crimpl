### [RemoteSlurmServer](RemoteSlurmServer.md).__init__ (function)


```py

def __init__(self, host, directory='~/crimpl', ssh='ssh', mail_user=None, server_name=None)

```



Connect to a remote server running a Slurm scheduler.

To create a new job, use [RemoteSlurmServer.create_job](RemoteSlurmServer.create_job.md) or to connect
to a previously created job, use [RemoteSlurmServer.get_job](RemoteSlurmServer.get_job.md).

Arguments
-----------
* `host` (string): host of the remote server.  Must be passwordless ssh-able.
    See [RemoteSlurmServer.host](RemoteSlurmServer.host.md)
* `directory` (string, optional, default='~/crimpl'): root directory of all
    jobs to run on the remote server.  The directory will be created
    if it does not already exist.
* `ssh` (string, optional, default='ssh'): command (and any arguments in
    addition to `host`) to ssh to the remote server.
* `mail_user` (string, optional, default=None): email to send notifications.
    If not provided or None, will default to the value in [RemoteSlurmServer.mail_user](RemoteSlurmServer.mail_user.md).
    Prepended to `script` as "#SBATCH --mail_user=mail_user"
* `server_name` (string): name to assign to the server.  If not provided,
    will be adopted automatically from `host` and available from
    [RemoteSlurmServer.server_name](RemoteSlurmServer.server_name.md).

