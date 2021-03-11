### [AWSEC2Job](AWSEC2Job.md).check_output (function)


```py

def check_output(self, server_path, local_path='./', wait_for_output=False, terminate_if_server_started=False)

```



Attempt to copy a file(s) back from the remote server.

Arguments
-----------
* `server_path` (string or list): path(s) (relative to `directory`) on the server
    of the file(s) to retrieve.  See &lt;AWSEC2Job.job_files&gt; for a list
    of available files on ther remote server.
* `local_path` (string, optional, default="./"): local path to copy
    the retrieved file.
* `wait_for_output` (bool, optional, default=False): NOT IMPLEMENTED
* `terminate_if_server_started` (bool, optional, default=False): whether
    the server EC2 instance should immediately be terminated if it
    was started in order to retrieve the files from the volume.
    The server EC2 instance can manually be terminated via
    &lt;AWSEC2Server.terminate&gt;.

Returns
----------
* None

