### [AWSEC2](AWSEC2.md).check_output (function)


```py

def check_output(self, server_path, local_path='./', wait_for_output=False, restart_if_necessary=True, stop_if_restarted=True)

```



Attempt to copy a file back from the server.

Arguments
-----------
* `server_path` (string): path on the server of the file to retrieve.
* `local_path` (string, optional, default="./"): local path to copy
    the retrieved file.
* `wait_for_output` (bool, optional, default=False): NOT IMPLEMENTED
* `restart_if_necessary` (bool, optional, default=True): start the server
    if it is not currently running.  This is particularly useful if
    `stop_on_complete` was sent to &lt;AWSEC2.submit_script&gt;.
* `stop_if_restarted` (bool, optional, default=True): if `restart_if_necessary`
    resulted in the need to start the server, then immediately stop it
    again.  Note that the server must manually be terminated (at some point,
    unless you're super rich) via &lt;AWSEC2.terminate&gt;.

Returns
----------
* None

