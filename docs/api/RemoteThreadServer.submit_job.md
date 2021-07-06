### [RemoteThreadServer](RemoteThreadServer.md).submit_job (function)


```py

def submit_job(self, script, files=[], job_name=None, conda_env=None, isolate_env=False, ignore_files=[], wait_for_job_status=False, trial_run=False)

```



Shortcut to [RemoteThreadServer.create_job](RemoteThreadServer.create_job.md) followed by [RemoteThreadJob.submit_script](RemoteThreadJob.submit_script.md).

Arguments
--------------
* `script`: passed to [RemoteThreadJob.submit_script](RemoteThreadJob.submit_script.md)
* `files`: passed to [RemoteThreadJob.submit_script](RemoteThreadJob.submit_script.md)
* `conda_env`: passed to [RemoteThreadServer.create_job](RemoteThreadServer.create_job.md)
* `isolate_env`: passed to [RemoteThreadServer.create_job](RemoteThreadServer.create_job.md)
* `ignore_files`: passed to [RemoteThreadJob.submit_script](RemoteThreadJob.submit_script.md)
* `wait_for_job_status`: passed to [RemoteThreadJob.submit_script](RemoteThreadJob.submit_script.md)
* `trial_run`: passed to [RemoteThreadJob.submit_script](RemoteThreadJob.submit_script.md)

Returns
--------------
* [RemoteThreadJob](RemoteThreadJob.md)

