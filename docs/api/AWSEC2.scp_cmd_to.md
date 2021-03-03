### [AWSEC2](AWSEC2.md).scp_cmd_to (property)




scp command to copy files to the server.

Returns
----------
* (string): command with "{}" placeholders for `local_path` and `server_path`.
    If the server is not yet started and &lt;AWSEC2.ip&gt; is not available,
    the ip will be replaced with {ip}

