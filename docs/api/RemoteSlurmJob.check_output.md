### [RemoteSlurmJob](RemoteSlurmJob.md).check_output (function)


```py

def check_output(self, server_path, local_path='./', wait_for_output=False)

```



Attempt to copy a file back from the server.

Arguments
-----------
* `server_path` (string or list): path(s) (relative to `directory`) on the server
    of the file(s) to retrieve.
* `local_path` (string, optional, default="./"): local path to copy
    the retrieved file.
* `wait_for_output` (bool, optional, default=False): NOT IMPLEMENTED


Returns
----------
* None

