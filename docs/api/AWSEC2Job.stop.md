### [AWSEC2Job](AWSEC2Job.md).stop (function)


```py

def stop(self, wait=True)

```



Stop the **job** EC2 instance.

Once stopped, the EC2 instance can be restarted via &lt;AWSEC2Job.start&gt;.

A stopped EC2 instance still results in charges for the storage, but no longer
charges for the CPU time.  See AWS pricing for more details.

Arguments
-------------
* `wait` (bool, optional, default=True): whether to wait for the server
    to reach a stopped &lt;AWSEC2Job.state&gt;.

Return
--------
* (string) &lt;AWSEC2Job.state&gt;

