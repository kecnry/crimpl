### [crimpl](crimpl.md).terminate_awsec2_instance (function)


```py

def terminate_awsec2_instance(instanceId)

```



Manually terminate an AWS EC2 instance by `instanceId`.

Usually this will be done via &lt;AWSEC2Server.terminate&gt; or &lt;AWSEC2Job.terminate&gt;.

Arguments
----------
* `instanceId` (string): AWS EC2 instanceId.  See &lt;list_awsec2_instances&gt;.

