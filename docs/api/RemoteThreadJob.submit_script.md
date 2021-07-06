### [RemoteThreadJob](RemoteThreadJob.md).submit_script (function)


```py

def submit_script(self, script, files=[], nprocs=None, ignore_files=[], wait_for_job_status=False, trial_run=False)

```



Submit a script to the server in the [RemoteThreadJob.conda_env](RemoteThreadJob.conda_env.md).

This will copy `script` (modified with the provided slurm options) and
`files` to [RemoteThreadJob.remote_directory](RemoteThreadJob.remote_directory.md) on the remote server and
run the script in a thread (without a scheduler).  To check on its status,
see [RemoteThreadJob.job_status](RemoteThreadJob.job_status.md).

To check on any expected output files, call [RemoteThreadJob.check_output](RemoteThreadJob.check_output.md).

See [RemoteThreadJob.run_script](RemoteThreadJob.run_script.md) to run a script and wait for it to complete.

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
* `ignore_files` (list, optional, default=[]): list of filenames on the
    remote server to ignore when calling [RemoteThreadJob.check_output](RemoteThreadJob.check_output.md)
* `wait_for_job_status` (bool or string or list, optional, default=False):
    Whether to wait for a specific job_status.  If True, will default to
    'complete'.  See also [RemoteThreadJob.wait_for_job_status](RemoteThreadJob.wait_for_job_status.md).
* `trial_run` (bool, optional, default=False): if True, the commands
    that would be sent to the server are returned but not executed.

Returns
------------
* [RemoteThreadJob](RemoteThreadJob.md)

Raises
------------
* ValueError: if a script has already been submitted within this
    [RemoteThreadJob](RemoteThreadJob.md) instance.
* TypeError: if `script` or `files` are not valid types.
* ValueError: if the files referened by `script` or `files` are not valid.

