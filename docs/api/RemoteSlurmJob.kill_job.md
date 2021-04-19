### [RemoteSlurmJob](RemoteSlurmJob.md).kill_job (function)


```py

def kill_job(self)

```



Kill a job by calling `scancel` on the remote server for
this job's [RemoteSlurmJob.slurm_id](RemoteSlurmJob.slurm_id.md).

Returns
-----------
* (string)

