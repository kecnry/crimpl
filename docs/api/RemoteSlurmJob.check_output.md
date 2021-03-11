### [RemoteSlurmJob](RemoteSlurmJob.md).check_output (function)


```py

def check_output(self, server_path=None, local_path='./', wait_for_output=False)

```



Attempt to copy a file(s) back from the remote server.

Arguments
-----------
* `server_path` (string or list or None, optional, default=None): path(s)
    (relative to `directory`) on the server of the file(s) to retrieve.
    If not provided or None, will default to [RemoteSlurmJob.output_files](RemoteSlurmJob.output_files.md).
    See also: [RemoteSlurmJob.ls](RemoteSlurmJob.ls.md) or [RemoteSlurmJob.job_files](RemoteSlurmJob.job_files.md) for a full list of
    available files on the remote server.
* `local_path` (string, optional, default="./"): local path to copy
    the retrieved file.
* `wait_for_output` (bool, optional, default=False): NOT IMPLEMENTED


Returns
----------
* None

