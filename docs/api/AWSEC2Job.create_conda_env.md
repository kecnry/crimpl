### [AWSEC2Job](AWSEC2Job.md).create_conda_env (function)


```py

def create_conda_env(self)

```



Create a conda environment (in the &lt;[Server](Server.md).remote_directory&gt;) named
&lt;AWSEC2Job.conda_env&gt;.

This environment will be available to any jobs in this server and will
be listed in &lt;[Server](Server.md).conda_envs&gt;.  The created environment will
use the same version of python as the local version and include pip
and numpy by default.

