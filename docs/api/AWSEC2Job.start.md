### [AWSEC2Job](AWSEC2Job.md).start (function)


```py

def start(self)

```



Start the **job** EC2 instance.

A running EC2 instance charges per CPU-second.  See AWS pricing for more details.

Note that &lt;AWSEC2.submit_script&gt; will automatically start the instance
if not already manually started.

Arguments
-------------

Return
--------
* (string) &lt;AWSEC2Job.state&gt;

