### [RemotePBSServer](RemotePBSServer.md).install_conda (function)


```py

def install_conda(self, in_server_directory=False)

```



Install conda on the remote server if it is not already installed.

See also:

* [RemotePBSServer.conda_installed](RemotePBSServer.conda_installed.md)

Arguments
-------------
* `in_server_directory` (bool, optional, default=False): whether to place
    the conda installation in [RemotePBSServer.directory](RemotePBSServer.directory.md) rather than the default
    user installation

Returns
------------
* (bool): output of [RemotePBSServer.conda_installed](RemotePBSServer.conda_installed.md)

