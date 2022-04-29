### [RemotePBSJob](RemotePBSJob.md).conda_env (property)




Name of the conda environment to use for any future calls
to [RemotePBSJob.run_script](RemotePBSJob.run_script.md) or [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md).

If the environment does not exist, it will be created during the next
call to [RemotePBSJob.run_script](RemotePBSJob.run_script.md) or [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md).

See also:

* RemotePBSJob.conda_env_exists&gt;
* [Server.conda_envs](Server.conda_envs.md)

Returns
-----------
* (str): name or path of the conda environment on the remote server.

