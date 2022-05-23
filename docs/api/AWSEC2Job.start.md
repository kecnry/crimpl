### [AWSEC2Job](AWSEC2Job.md).start (function)


```py

def start(self, wait=True)

```



Start the **job** EC2 instance.

A running EC2 instance charges per CPU-second.  See AWS pricing for more details.

Note that &lt;AWSEC2.submit_script&gt; will automatically start the instance
if not already manually started.

Arguments
------------
* `wait` (bool, optional, default=True): `wait` is required to be True
    in order to attach the **server** volume and is only exposed as a
    kwarg for consistent calling signature (the passed value will be ignored)

Return
--------
* (string) &lt;AWSEC2Job.state&gt;

