### [AWSEC2](AWSEC2.md).start (function)


```py

def start(self, wait=True)

```



Start the server.

A running server charges per CPU-second.  See AWS pricing for more details.

Note that &lt;AWSEC2.submit_script&gt; will automatically start the server
if not already manually started.

Arguments
-------------
* `wait` (bool, optional, default=False): whether to wait for the server
    to reach a running &lt;AWSEC2.state&gt; (and an additional 30 seconds
    to allow for initialization checks to complete and for the server
    to be ready for commands).

Return
--------
* (string) &lt;AWSEC2.state&gt;

