### [LocalThreadServer](LocalThreadServer.md).submit_job (function)


```py

def submit_job(self, script, files=[], job_name=None, conda_env=None, isolate_env=False, ignore_files=[], wait_for_job_status=False, trial_run=False)

```



Shortcut to [LocalThreadServer.create_job](LocalThreadServer.create_job.md) followed by [LocalThreadJob.submit_script](LocalThreadJob.submit_script.md).

Arguments
--------------
* `script`: passed to [LocalThreadJob.submit_script](LocalThreadJob.submit_script.md)
* `files`: passed to [LocalThreadJob.submit_script](LocalThreadJob.submit_script.md)
* `job_name`: passed to [LocalThreadServer.create_job](LocalThreadServer.create_job.md)
* `conda_env`: passed to [LocalThreadServer.create_job](LocalThreadServer.create_job.md)
* `isolate_env`: passed to [LocalThreadServer.create_job](LocalThreadServer.create_job.md)
* `ignore_files`: passed to [LocalThreadJob.submit_script](LocalThreadJob.submit_script.md)
* `wait_for_job_status`: passed to [LocalThreadJob.submit_script](LocalThreadJob.submit_script.md)
* `trial_run`: passed to [LocalThreadJob.submit_script](LocalThreadJob.submit_script.md)

Returns
--------------
* [LocalThreadJob](LocalThreadJob.md)

