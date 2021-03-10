### [AWSEC2Server](AWSEC2Server.md).run_script (function)


```py

def run_script(self, script, files=[], trial_run=False)

```



Run a script on the **server** EC2 instance (single processor),
and wait for it to complete.

The files are copied and executed in &lt;AWSEC2Server.directory&gt; directly
(whereas &lt;AWSEC2Job&gt; scripts are executed in subdirectories).

This is useful for installation scripts, setting up virtual environments,
etc, as the **server** EC2 instance only runs a single processor.  Once
complete, setup a job with &lt;AWSEC2Server.create_job&gt; or &lt;AWSEC2Server.get_job&gt;
to submit the compute job on more resources (via &lt;AWSEC2Job.run_script&gt;
or &lt;AWSEC2.submit_script&gt;).

Arguments
----------------
* `script` (string or list): shell script to run on the remote server,
    including any necessary installation steps.  Note that the script
    can call any other scripts in `files`.  If a string, must be the
    path of a valid file which will be copied to the server.  If a list,
    must be a list of commands (i.e. a newline will be placed between
    each item in the list and sent as a single script to the server).
* `files` (list, optional, default=[]): list of paths to additional files
    to copy to the server required in order to successfully execute
    `script`.
* `trial_run` (bool, optional, default=False): if True, the commands
    that would be sent to the server are returned but not executed
    (and the server is not started automatically - so these may include
    an [ip](ip.md) placeholder).


Returns
------------
* None

Raises
------------
* TypeError: if `script` or `files` are not valid types.
* ValueError: if the files referened by `script` or `files` are not valid.

