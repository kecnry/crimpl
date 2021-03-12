### [AWSEC2Job](AWSEC2Job.md).check_output (function)


```py

def check_output(self, server_path=None, local_path='./', terminate_if_server_started=False)

```



Attempt to copy a file(s) back from the remote server.

Arguments
-----------
* `server_path` (string or list or None, optional, default=None): path(s)
    (relative to `directory`) on the server of the file(s) to retrieve.
    If not provided or None, will default to &lt;AWSEC2Job.output_files&gt;.
    See also: &lt;AWSEC2Job.ls&gt; or &lt;AWSEC2Job.job_files&gt; for a full list of
    available files on the remote server.
* `local_path` (string, optional, default="./"): local path to copy
    the retrieved file.
* `terminate_if_server_started` (bool, optional, default=False): whether
    the server EC2 instance should immediately be terminated if it
    was started in order to retrieve the files from the volume.
    The server EC2 instance can manually be terminated via
    &lt;AWSEC2Server.terminate&gt;.

Returns
----------
* None

