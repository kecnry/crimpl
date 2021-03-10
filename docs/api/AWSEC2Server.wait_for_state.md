### [AWSEC2Server](AWSEC2Server.md).wait_for_state (function)


```py

def wait_for_state(self, state, sleeptime=0.5)

```



Wait for the **server** EC2 instance to reach a specified state.

Arguments
----------
* `state` (string): the desired state.
* `sleeptime` (float, optional, default): seconds to wait between
    successive state checks.

Returns
----------
* (string) &lt;AWSEC2Server.state&gt;

