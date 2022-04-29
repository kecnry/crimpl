### [RemotePBSServer](RemotePBSServer.md).__init__ (function)


```py

def __init__(self, host, directory='~/crimpl', ssh='ssh', scp='scp', mail_user=None, server_name=None)

```



Connect to a remote server running a PBS scheduler.

To create a new job, use [RemotePBSServer.create_job](RemotePBSServer.create_job.md) or to connect
to a previously created job, use [RemotePBSServer.get_job](RemotePBSServer.get_job.md).

Arguments
-----------
* `host` (string): host of the remote server.  Must be passwordless ssh-able.
    See [RemotePBSServer.host](RemotePBSServer.host.md)
* `directory` (string, optional, default='~/crimpl'): root directory of all
    jobs to run on the remote server.  The directory will be created
    if it does not already exist.
* `ssh` (string, optional, default='ssh'): command (and any arguments in
    addition to `host`) to ssh to the remote server.
* `scp` (string, optional, default='scp'): command (and any arguments)
    to copy files to the remote server.
* `mail_user` (string, optional, default=None): email to send notifications.
    If not provided or None, will default to the value in [RemotePBSServer.mail_user](RemotePBSServer.mail_user.md).
    Prepended to `script` as "#PBS -M mail_user"
* `server_name` (string): name to assign to the server.  If not provided,
    will be adopted automatically from `host` and available from
    [RemotePBSServer.server_name](RemotePBSServer.server_name.md).

