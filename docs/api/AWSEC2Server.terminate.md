### [AWSEC2Server](AWSEC2Server.md).terminate (function)


```py

def terminate(self, wait=True, delete_volume=False)

```



Terminate the **server** EC2 instance.

Once terminated, the EC2 instance cannot be restarted, but will no longer
result in charges.  See also &lt;AWSEC2Server.stop&gt; and AWS pricing for more details.

Arguments
-------------
* `wait` (bool, optional, default=True): whether to wait for the server
    to reach a terminated &lt;AWSEC2Server.state&gt;.

Return
--------
* (string) &lt;AWSEC2Server.state&gt;

