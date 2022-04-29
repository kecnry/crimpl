### [RemotePBSJob](RemotePBSJob.md).check_output (function)


```py

def check_output(self, server_path=None, local_path='./')

```



Attempt to copy a file(s) back from the remote server.

Arguments
-----------
* `server_path` (string or list or None, optional, default=None): path(s)
    (relative to `directory`) on the server of the file(s) to retrieve.
    If not provided or None, will default to [RemotePBSJob.output_files](RemotePBSJob.output_files.md).
    See also: [RemotePBSJob.ls](RemotePBSJob.ls.md) or [RemotePBSJob.job_files](RemotePBSJob.job_files.md) for a full list of
    available files on the remote server.
* `local_path` (string, optional, default="./"): local path to copy
    the retrieved file.


Returns
----------
* (list) list of retrieved files

