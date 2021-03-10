### [AWSEC2Server](AWSEC2Server.md).scp_cmd_to (property)




scp command to copy files to the **server** EC2 instance (or a child **job** EC2 instance
if the **server** EC2 instance is not running).

Returns
----------
* (string): command with "{}" placeholders for `local_path` and `server_path`.
    If the server is not yet started and &lt;AWSEC2Server.ip&gt; is not available,
    the ip will be replaced with {ip}

