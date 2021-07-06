### [RemoteThreadJob](RemoteThreadJob.md).conda_env (property)




Name of the conda environment to use for any future calls
to [RemoteThreadJob.run_script](RemoteThreadJob.run_script.md) or [RemoteThreadJob.submit_script](RemoteThreadJob.submit_script.md).

If the environment does not exist, it will be created during the next
call to [RemoteThreadJob.run_script](RemoteThreadJob.run_script.md) or [RemoteThreadJob.submit_script](RemoteThreadJob.submit_script.md).

See also:

* RemoteThreadJob.conda_env_exists&gt;
* [Server.conda_envs](Server.conda_envs.md)

Returns
-----------
* (str): name or path of the conda environment on the remote server.

