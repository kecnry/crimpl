### [AWSEC2Server](AWSEC2Server.md).conda_envs (property)




List (existing) available conda environments and their paths on the remote server.

These will include those created at the root level (either within or outside crimpl)
as well as those created by this &lt;AWSEC2Server&gt; (which are stored in &lt;AWSEC2Server.directory&gt;).
In the case where the same name is available at the root level and created by
this &lt;AWSEC2Server&gt;, the one created by &lt;AWSEC2Server&gt; will take precedence.

Returns
--------
* (list)

