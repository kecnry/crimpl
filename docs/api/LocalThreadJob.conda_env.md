### [LocalThreadJob](LocalThreadJob.md).conda_env (property)




Name of the conda environment to use for any future calls
to [LocalThreadJob.run_script](LocalThreadJob.run_script.md) or [LocalThreadJob.submit_script](LocalThreadJob.submit_script.md).

If the environment does not exist, it will be created during the next
call to [LocalThreadJob.run_script](LocalThreadJob.run_script.md) or [LocalThreadJob.submit_script](LocalThreadJob.submit_script.md).

See also:

* LocalThreadJob.conda_env_exists&gt;
* [Server.conda_envs](Server.conda_envs.md)

Returns
-----------
* (str): name or path of the conda environment on the remote server.

