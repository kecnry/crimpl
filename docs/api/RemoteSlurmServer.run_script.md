### [RemoteSlurmServer](RemoteSlurmServer.md).run_script (function)


```py

def run_script(self, script, files=[], conda_environment=None, trial_run=False)

```



Run a script on the server in the `conda_environment`, and wait for it to complete.

The files are copied and executed in [RemoteSlurmServer.directory](RemoteSlurmServer.directory.md) directly
(whereas [RemoteSlurmJob](RemoteSlurmJob.md) scripts are executed in subdirectories).

This is useful for short installation/setup scripts that do not belong
in the scheduled job.

The resulting `script` and `files` are copied to [RemoteSlurmServer.directory](RemoteSlurmServer.directory.md)
on the remote server and then `script` is executed via ssh.

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
* `conda_environment` (string or None): name of the conda environment to
    run the script, or None to use the 'default' environment stored in
    the server crimpl directory.
* `trial_run` (bool, optional, default=False): if True, the commands
    that would be sent to the server are returned but not executed.


Returns
------------
* None

Raises
------------
* TypeError: if `script` or `files` are not valid types.
* ValueError: if the files referened by `script` or `files` are not valid.

