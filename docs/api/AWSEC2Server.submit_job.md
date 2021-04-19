### [AWSEC2Server](AWSEC2Server.md).submit_job (function)


```py

def submit_job(self, script, files=[], job_name=None, conda_environment=None, isolate_environment=False, nprocs=4, terminate_on_complete=True, ignore_files=[], wait_for_job_status=False, trial_run=False)

```



Shortcut to &lt;AWSEC2Server.create_job&gt; followed by &lt;AWSEC2Job.submit_script&gt;.

Arguments
--------------
* `script`: passed to &lt;AWSEC2Job.submit_script&gt;
* `files`: passed to &lt;AWSEC2Job.submit_script&gt;
* `job_name`: passed to &lt;AWSEC2Server.create_job&gt;
* `conda_environment`: passed to &lt;AWSEC2Server.create_job&gt;
* `isolate_environment`: passed to &lt;AWSEC2Server.create_job&gt;
* `nprocs`: passed to &lt;AWSEC2Server.create_job&gt;
* `terminate_on_complete`: passed to &lt;AWSEC2Job.submit_script&gt;
* `ignore_files`: passed to &lt;AWSEC2Job.submit_script&gt;
* `wait_for_job_status`: passed to &lt;AWSEC2Job.submit_script&gt;
* `trial_run`: passed to &lt;AWSEC2Job.submit_script&gt;

Returns
--------------
* &lt;AWSEC2Job&gt;

