### [RemoteSlurmJob](RemoteSlurmJob.md).create_conda_environment (function)


```py

def create_conda_environment(self)

```



Create a conda environment (in the &lt;[Server](Server.md).remote_directory&gt;) named
[RemoteSlurmJob.conda_environment](RemoteSlurmJob.conda_environment.md).

This environment will be available to any jobs in this server and will
be listed in &lt;[Server](Server.md).conda_environments&gt;.  The created environment will
use the same version of python as the local version and include both
pip and numpy, by default.

