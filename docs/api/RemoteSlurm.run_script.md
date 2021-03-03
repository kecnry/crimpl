### [RemoteSlurm](RemoteSlurm.md).run_script (function)


```py

def run_script(self, script, files=[], trial_run=False)

```



Run a script on the server, and wait for it to complete.

This is useful for short installation/setup scripts that do not belong
in the scheduled job.

See [RemoteSlurm.submit_script](RemoteSlurm.submit_script.md) to submit a script via the slurm scheduler
and leave running in the background on the server.

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
    that would be sent to the server are returned but not executed.


Returns
------------
* None

Raises
------------
* TypeError: if `script` or `files` are not valid types.
* ValueError: if the files referened by `script` or `files` are not valid.

