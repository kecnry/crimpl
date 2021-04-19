### [RemoteSlurmJob](RemoteSlurmJob.md).conda_env (property)




Name of the conda environment to use for any future calls
to [RemoteSlurmJob.run_script](RemoteSlurmJob.run_script.md) or [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md).

If the environment does not exist, it will be created during the next
call to [RemoteSlurmJob.run_script](RemoteSlurmJob.run_script.md) or [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md).

See also:

* RemoteSlurmJob.conda_env_exists&gt;
* [Server.conda_envs](Server.conda_envs.md)

Returns
-----------
* (str): name or path of the conda environment on the remote server.

