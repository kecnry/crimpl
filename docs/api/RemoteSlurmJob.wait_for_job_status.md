### [RemoteSlurmJob](RemoteSlurmJob.md).wait_for_job_status (function)


```py

def wait_for_job_status(self, status='complete', sleeptime=5)

```



Wait for the job to reach a desired job_status.

Arguments
-----------
* `status` (string or list, optional, default='complete'): status
    or statuses to exit the wait loop.
* `sleeptime` (int, optional, default=5): number of seconds to wait
    between successive job status checks.

Returns
----------
* (string): `status`

