### [AWSEC2](AWSEC2.md).stop (function)


```py

def stop(self, wait=False)

```



Stop the server.

Once stopped, the server can be restarted via &lt;AWSEC2.start&gt;, including
by creating a new &lt;AWSEC2&gt; instance with the correct &lt;AWSEC2.instanceId&gt;.

A stopped server still results in charges for the storage, but no longer
charges for the CPU time.  See AWS pricing for more details.

Arguments
-------------
* `wait` (bool, optional, default=False): whether to wait for the server
    to reach a stopped &lt;AWSEC2.state&gt;.

Return
--------
* (string) &lt;AWSEC2.state&gt;

