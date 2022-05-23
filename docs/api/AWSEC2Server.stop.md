### [AWSEC2Server](AWSEC2Server.md).stop (function)


```py

def stop(self, wait=True)

```



Stop the **server** EC2 instance.

Once stopped, the EC2 instance can be restarted via &lt;AWSEC2Server.start&gt;, including
by creating a new &lt;AWSEC2Server&gt; instance with the correct &lt;AWSEC2Server.instanceId&gt;.

A stopped EC2 instance still results in charges for the storage, but no longer
charges for the CPU time.  See AWS pricing for more details.

Arguments
-------------
* `wait` (bool, optional, default=True): whether to wait for the server
    to reach a stopped &lt;AWSEC2Server.state&gt;.

Return
--------
* (string) &lt;AWSEC2Server.state&gt;

