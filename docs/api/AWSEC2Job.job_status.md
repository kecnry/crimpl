### [AWSEC2Job](AWSEC2Job.md).job_status (property)




Return the status of the job.

If a job has been submitted, but the EC2 instance no longer exists or has
been stopped or terminated, then the job is assumed to have completed
(although in reality it may have failed or the EC2 instance terminated
manually).

If the EC2 instance is running, then the status file in the job-directory
is checked and will return either 'running' or 'complete'.


Returns
-----------
* (string): one of not-submitted, running, complete, unknown

