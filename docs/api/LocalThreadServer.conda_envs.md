### [LocalThreadServer](LocalThreadServer.md).conda_envs (property)




List (existing) available conda environments and their paths on the remote server.

These will include those created at the root level (either within or outside crimpl)
as well as those created by this [LocalThreadServer](LocalThreadServer.md) (which are stored in [LocalThreadServer.directory](LocalThreadServer.directory.md)).
In the case where the same name is available at the root level and created by
this [LocalThreadServer](LocalThreadServer.md), the one created by [LocalThreadServer](LocalThreadServer.md) will take precedence.

Returns
--------
* (list)

