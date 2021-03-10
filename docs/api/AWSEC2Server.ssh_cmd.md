### [AWSEC2Server](AWSEC2Server.md).ssh_cmd (property)




ssh command to the **server** EC2 instance (or a child **job** EC2 instance
if the **server** EC2 instance is not running).

Returns
----------
* (string): If the server is not yet started and &lt;AWSEC2Server.ip&gt; is not available,
    the ip will be replaced with {ip}

