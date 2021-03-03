### [AWSEC2](AWSEC2.md).terminate (function)


```py

def terminate(self, wait=False)

```



Terminate the server.

Once terminated, the server cannot be restarted, but will no longer
result in charges.  See also &lt;AWSEC2.stop&gt; and AWS pricing for more details.

Arguments
-------------
* `wait` (bool, optional, default=False): whether to wait for the server
    to reach a terminated &lt;AWSEC2.state&gt;.

Return
--------
* (string) &lt;AWSEC2.state&gt;

