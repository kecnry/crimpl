### [AWSEC2Server](AWSEC2Server.md).delete_volume (function)


```py

def delete_volume(self, terminate_instances=True)

```



Delete the AWS EC2 **server** volume.  Once deleted, servers and jobs
will no longer be accessible and a new &lt;AWSEC2Server&gt; instance must be created
for additional submissions.

If `terminate_instances` is True (as it is by default), any EC2 instances
in &lt;crimpl.list_awsec2_instances&gt; with this &lt;AWSEC2Server.server_name&gt;
will be terminated first.

Arguments
----------
* `terminate_instances` (bool, optional, default=True): whether to first
    check for any non-terminated **server** or **job** EC2 instances
    and terminate them.

Returns
-----------
* None

