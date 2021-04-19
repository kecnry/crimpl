### [AWSEC2Job](AWSEC2Job.md).conda_env (property)




Name of the conda environment to use for any future calls
to &lt;AWSEC2Job.run_script&gt; or &lt;AWSEC2Job.submit_script&gt;.

If the environment does not exist, it will be created during the next
call to &lt;AWSEC2Job.run_script&gt; or &lt;AWSEC2Job.submit_script&gt;.

See also:

* AWSEC2Job.conda_env_exists&gt;
* [Server.conda_envs](Server.conda_envs.md)

Returns
-----------
* (str): name or path of the conda environment on the remote server.

