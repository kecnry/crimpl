### [AWSEC2Server](AWSEC2Server.md).__init__ (function)


```py

def __init__(self, server_name=None, volumeSize=4, volumeId=None, instanceId=None, KeyFile=None, KeyName=None, SubnetId=None, SecurityGroupId=None)

```



Connect to an existing &lt;AWSEC2Server&gt; by `volumeId`.

To create a new server, use &lt;AWSEC2Server.new&gt; instead.

* `server_name` (string, optional, default=None): internal name of the
    **existing** server to retrieve.  To create a new server, call
    &lt;AWSEC2Server.new&gt; instead.  Either `server_name` or `volumeId` must
    be provided.
* `volumeSize` (int, optional, default=4): size, in GiB of the shared
    volume to create.  Once created, the volume begins accruing charges.
    See AWS documentation for pricing details.  Will be ignored if volume
    already exists.
* `volumeId` (string, optional, default=None): AWS internal `volumeId`
    of the shared AWS EC2 volume instance.  Either `server_name` or
    `volumeId` must be provided.
* `instanceId` (string, optional, default=None): AWS internal `instanceId`
    of the **server** EC2 instance.  If not provided, will be determined
    from `server_name` and/or `volumeId`.
* `KeyFile` (string, required, default=None): path to the KeyFile
* `KeyName` (string, optional, default=None): AWS internal name corresponding
    to `KeyFile`.  If not provided, will be assumed to be `basename(KeyFile).split(.)[0]`.
* `SubnetId` (string, required, default=None):
* `SecurityGroupId` (string, required, default=None):

Returns
------------
* &lt;AWSEC2Server&gt;

