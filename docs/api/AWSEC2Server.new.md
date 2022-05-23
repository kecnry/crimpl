### [AWSEC2Server](AWSEC2Server.md).new (method)


```py

def new(cls, server_name=None, volumeSize=4, KeyFile=None, KeyName=None, SubnetId=None, SecurityGroupId=None)

```



Create a new &lt;AWSEC2Server&gt; instance.

This creates a blank AWS EC2 volume to be shared among both **server**
and **job** AWS EC2 instances with `volumeSize` storage.

Arguments
-----------
* `server_name` (string, optional, default=None): internal name to assign
    to the server.  If not provided, will be assigned automatically and
    available from &lt;AWSEC2Server.server_name&gt;.  Once created, the &lt;AWSEC2Server&gt;
    object can then be retrieved by name via &lt;AWSEC2Server.__init__&gt;.
* `volumeSize` (int, optional, default=4): size, in GiB of the shared
    volume to create.  Once created, the volume begins accruing charges.
    See AWS documentation for pricing details.
* `KeyFile` (string, required, default=None): path to the KeyFile
* `KeyName` (string, optional, default=None): AWS internal name corresponding
    to `KeyFile`.  If not provided, will be assumed to be `basename(KeyFile).split(.)[0]`.
* `SubnetId` (string, required, default=None):
* `SecurityGroupId` (string, required, default=None):

Returns
----------
* &lt;AWSEC2Server&gt;

