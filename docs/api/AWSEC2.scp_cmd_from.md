### [AWSEC2](AWSEC2.md).scp_cmd_from (property)




scp command to copy files from the server.

Returns
----------
* (string): command with "{}" placeholders for `server_path` and `local_path`.
    If the server is not yet started and &lt;AWSEC2.ip&gt; is not available,
    the ip will be replaced with {ip}

