### [crimpl](crimpl.md).load_server (function)


```py

def load_server(name)

```



Load a server configuration from disk.

Returns
----------
* the appropriate server object ([LocalThreadServer](LocalThreadServer.md), [RemoteThreadServer](RemoteThreadServer.md),
    [RemoteSlurmServer](RemoteSlurmServer.md), [RemotePBSServer](RemotePBSServer.md), &lt;AWSEC2Server&gt;)

