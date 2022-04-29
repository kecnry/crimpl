### [RemotePBSServer](RemotePBSServer.md).submit_job (function)


```py

def submit_job(self, script, files=[], job_name=None, pbs_job_name=None, conda_env=None, isolate_env=False, nnodes=1, nprocs=4, walltime='2-00:00:00', mail_type='END,FAIL', mail_user=None, ignore_files=[], wait_for_job_status=False, trial_run=False)

```



Shortcut to [RemotePBSServer.create_job](RemotePBSServer.create_job.md) followed by [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md).

Arguments
--------------
* `script`: passed to [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md)
* `files`: passed to [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md)
* `job_name`: passed to [RemotePBSServer.create_job](RemotePBSServer.create_job.md)
* `pbs_job_name`: passed to [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md)
* `conda_env`: passed to [RemotePBSServer.create_job](RemotePBSServer.create_job.md)
* `isolate_env`: passed to [RemotePBSServer.create_job](RemotePBSServer.create_job.md)
* `nnodes`: passed to [RemotePBSServer.create_job](RemotePBSServer.create_job.md)
* `nprocs`: passed to [RemotePBSServer.create_job](RemotePBSServer.create_job.md)
* `walltime`: passed to [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md)
* `mail_type`: passed to [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md)
* `mail_user`: passed to [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md)
* `ignore_files`: passed to [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md)
* `wait_for_job_status`: passed to [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md)
* `trial_run`: passed to [RemotePBSJob.submit_script](RemotePBSJob.submit_script.md)

Returns
--------------
* [RemotePBSJob](RemotePBSJob.md)

