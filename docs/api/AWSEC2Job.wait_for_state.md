### [AWSEC2Job](AWSEC2Job.md).wait_for_state (function)


```py

def wait_for_state(self, state='running', error_if=[], sleeptime=0.5)

```



Wait for the **job** EC2 instance to reach a specified state.

Arguments
----------
* `state` (string or list, optional, default='running'): state or states
    to exit the wait loop successfully.
* `error_if` (string or list, optional, default=[]): state or states
    to exit the wait loop and raise an error.
* `sleeptime` (float, optional, default): seconds to wait between
    successive state checks.

Returns
----------
* (string) &lt;AWSEC2Job.state&gt;

