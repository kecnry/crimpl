### [RemoteSlurmServer](RemoteSlurmServer.md).submit_job (function)


```py

def submit_job(self, script, files=[], job_name=None, slurm_job_name=None, conda_environment=None, isolate_environment=False, nprocs=4, walltime='2-00:00:00', mail_type='END,FAIL', mail_user=None, ignore_files=[], wait_for_job_status=False, trial_run=False)

```



Shortcut to [RemoteSlurmServer.create_job](RemoteSlurmServer.create_job.md) followed by [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md).

Arguments
--------------
* `script`: passed to [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md)
* `files`: passed to [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md)
* `job_name`: passed to [RemoteSlurmServer.create_job](RemoteSlurmServer.create_job.md)
* `slurm_job_name`: passed to [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md)
* `conda_environment`: passed to [RemoteSlurmServer.create_job](RemoteSlurmServer.create_job.md)
* `isolate_environment`: passed to [RemoteSlurmServer.create_job](RemoteSlurmServer.create_job.md)
* `nprocs`: passed to [RemoteSlurmServer.create_job](RemoteSlurmServer.create_job.md)
* `walltime`: passed to [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md)
* `mail_type`: passed to [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md)
* `mail_user`: passed to [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md)
* `ignore_files`: passed to [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md)
* `wait_for_job_status`: passed to [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md)
* `trial_run`: passed to [RemoteSlurmJob.submit_script](RemoteSlurmJob.submit_script.md)

Returns
--------------
* [RemoteSlurmJob](RemoteSlurmJob.md)

