### [RemotePBSServer](RemotePBSServer.md).conda_envs (property)




List (existing) available conda environments and their paths on the remote server.

These will include those created at the root level (either within or outside crimpl)
as well as those created by this [RemotePBSServer](RemotePBSServer.md) (which are stored in [RemotePBSServer.directory](RemotePBSServer.directory.md)).
In the case where the same name is available at the root level and created by
this [RemotePBSServer](RemotePBSServer.md), the one created by [RemotePBSServer](RemotePBSServer.md) will take precedence.

Returns
--------
* (list)

