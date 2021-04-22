### [LocalThreadServer](LocalThreadServer.md).install_conda (function)


```py

def install_conda(self, in_server_directory=False)

```



Install conda on the remote server if it is not already installed.

See also:

* [LocalThreadServer.conda_installed](LocalThreadServer.conda_installed.md)

Arguments
-------------
* `in_server_directory` (bool, optional, default=False): whether to place
    the conda installation in [LocalThreadServer.directory](LocalThreadServer.directory.md) rather than the default
    user installation

Returns
------------
* (bool): output of [LocalThreadServer.conda_installed](LocalThreadServer.conda_installed.md)

