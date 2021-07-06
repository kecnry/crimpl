### [RemoteThreadServer](RemoteThreadServer.md).install_conda (function)


```py

def install_conda(self, in_server_directory=False)

```



Install conda on the remote server if it is not already installed.

See also:

* [RemoteThreadServer.conda_installed](RemoteThreadServer.conda_installed.md)

Arguments
-------------
* `in_server_directory` (bool, optional, default=False): whether to place
    the conda installation in [RemoteThreadServer.directory](RemoteThreadServer.directory.md) rather than the default
    user installation

Returns
------------
* (bool): output of [RemoteThreadServer.conda_installed](RemoteThreadServer.conda_installed.md)

