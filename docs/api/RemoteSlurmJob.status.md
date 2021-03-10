### [RemoteSlurmJob](RemoteSlurmJob.md).status (property)




Return the status of the job by calling and parsing the output of
[RemoteSlurmJob.squeue](RemoteSlurmJob.squeue.md).

If the job is no longer available in the queue, it is assumed to have
completed (although in reality, it may have failed or been canceled).

Returns
-----------
* (string)

