### [LocalThreadServer](LocalThreadServer.md).run_script (function)


```py

def run_script(self, script, files=[], conda_env=None, trial_run=False)

```



Run a script in the server directory in the `conda_env`, and wait for it to complete.

The files are copied and executed in [LocalThreadServer.directory](LocalThreadServer.directory.md) directly
(whereas [LocalThreadJob](LocalThreadJob.md) scripts are executed in subdirectories).

This is useful for short installation/setup scripts that do not belong
in the scheduled job.

The resulting `script` and `files` are copied to [LocalThreadServer.directory](LocalThreadServer.directory.md)
and then `script` is executed.

Arguments
----------------
* `script` (string or list): shell script to run in the server directory,
    including any necessary installation steps.  Note that the script
    can call any other scripts in `files`.  If a string, must be the
    path of a valid file which will be copied to the server.  If a list,
    must be a list of commands (i.e. a newline will be placed between
    each item in the list and sent as a single script to the server).
* `files` (list, optional, default=[]): list of paths to additional files
    to copy to the server directory required in order to successfully execute
    `script`.
* `conda_env` (string or None, optional, default=None): name of
    the conda environment to run the script or False to not use a
    conda environment.  If not passed or None, will default to 'default'
    if conda is installed on the server or to False otherwise.
* `trial_run` (bool, optional, default=False): if True, the commands
    that would be sent to the server are returned but not executed.


Returns
------------
* None

Raises
------------
* TypeError: if `script` or `files` are not valid types.
* ValueError: if the files referened by `script` or `files` are not valid.

