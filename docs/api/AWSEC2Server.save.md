### [AWSEC2Server](AWSEC2Server.md).save (function)


```py

def save(self, name=None, overwrite=False)

```



Save this server configuration to ~/.crimpl to be loaded again via
[crimpl.load_server](crimpl.load_server.md).

Note that this saves everything in &lt;AWSEC2Server.to_dict&gt; to disk in ASCII.

Arguments
----------
* `name` (string, optional, default=None): name of the server.  Will
    default to &lt;AWSEC2Server.server_name&gt; if set.
* `overwrite` (bool, optional, default=False): whether to overwrite
    an existing saved configuration for `name`.

Returns
----------
* (string): path to the saved ascii file

Raises
----------
* ValueError: if `name` is already saved but `overwrite` is not passed as True

