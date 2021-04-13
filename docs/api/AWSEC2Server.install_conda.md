### [AWSEC2Server](AWSEC2Server.md).install_conda (function)


```py

def install_conda(self, in_server_directory=False)

```



Install conda on the remote server if it is not already installed.

See also:

* &lt;AWSEC2Server.conda_installed&gt;

Arguments
-------------
* `in_server_directory` (bool, optional, default=False): whether to place
    the conda installation in &lt;AWSEC2Server.directory&gt; rather than the default
    user installation

Returns
------------
* (bool): output of &lt;AWSEC2Server.conda_installed&gt;

