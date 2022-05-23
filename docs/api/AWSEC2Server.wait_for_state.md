### [AWSEC2Server](AWSEC2Server.md).wait_for_state (function)


```py

def wait_for_state(self, state='running', sleeptime=0.5)

```



Wait for the **server** EC2 instance to reach a specified state.

Arguments
----------
* `state` (string or list, optional, default='running'): state or states
    to exit the wait loop successfully.
* `error_if` (string or list, optional, default=[]): state or states
    to exit the wait loop and raise an error.
* `sleeptime` (float, optional, default=5): number of seconds to wait
    between successive EC2 state checks.

Returns
----------
* (string) &lt;AWSEC2Server.state&gt;

