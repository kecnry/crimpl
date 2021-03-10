### [AWSEC2Job](AWSEC2Job.md).run_script (function)


```py

def run_script(self, script, files=[], trial_run=False)

```



Run a script on the **job** server, and wait for it to complete.

See &lt;AWSEC2Job.submit_script&gt; to submit a script to leave running in the background.

For scripts that only require one processor and may take some time (i.e.
installation and setup script), consider using &lt;AWSEC2Server.submit_script&gt;
before initializing the **job** EC2 instance.

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

