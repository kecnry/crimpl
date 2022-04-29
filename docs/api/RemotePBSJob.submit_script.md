### [RemotePBSJob](RemotePBSJob.md).submit_script (function)


```py

def submit_script(self, script, files=[], pbs_job_name=None, nnodes=1, nprocs=None, walltime='2-00:00:00', mail_type='ae', mail_user=None, ignore_files=[], wait_for_job_status=False, trial_run=False)

```



Submit a script to the server in the [RemotePBSJob.conda_env](RemotePBSJob.conda_env.md).

This will copy `script` (modified with the provided slurm options) and
`files` to [RemotePBSJob.remote_directory](RemotePBSJob.remote_directory.md) on the remote server and
submit the script to the PBS scheduler.  To check on its status,
see [RemotePBSJob.job_status](RemotePBSJob.job_status.md).

Additional PBS customization (not included in the keyword arguments
listed below) can be included in the beginning of the script.

To check on any expected output files, call [RemotePBSJob.check_output](RemotePBSJob.check_output.md).

See [RemotePBSJob.run_script](RemotePBSJob.run_script.md) to run a script and wait for it to complete.

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
* `pbs_job_name` (string, optional, default=None): name of the job within PBS.
    Prepended to `script` as "#PBS -N jobname".  Defaults to
    [RemotePBSJob.job_name](RemotePBSJob.job_name.md).
* `nnodes` (int, optional, default=1): number of nodes to run the
    job.  Prepended to `script` as "#PBS -l nodes=nnodes".
* `nprocs` (int, optional, default=None): number of processors (per node) to run the
    job.  Prepended to `script` as "#PBS -l ppn=nprocs".  If None, will
    default to the `nprocs` set when creating the [RemotePBSJob](RemotePBSJob.md) instance.
    See [RemotePBSJob.nprocs](RemotePBSJob.nprocs.md).
* `walltime` (string, optional, default='2-00:00:00'): maximum walltime
    to schedule the job.  Prepended to `script` as "#PBS -l walltime=walltime".
* `mail_type` (string, optional, default='ae'): conditions to notify
    by email to `mail_user`.  Prepended to `script` as "#PBS -m mail_type".
* `mail_user` (string, optional, default=None): email to send notifications.
    If not provided or None, will default to the value in [RemotePBSServer.mail_user](RemotePBSServer.mail_user.md).
    Prepended to `script` as "#PBS -M mail_user"
* `ignore_files` (list, optional, default=[]): list of filenames on the
    remote server to ignore when calling [RemotePBSJob.check_output](RemotePBSJob.check_output.md)
* `wait_for_job_status` (bool or string or list, optional, default=False):
    Whether to wait for a specific job_status.  If True, will default to
    'complete'.  See also [RemotePBSJob.wait_for_job_status](RemotePBSJob.wait_for_job_status.md).
* `trial_run` (bool, optional, default=False): if True, the commands
    that would be sent to the server are returned but not executed.

Returns
------------
* [RemotePBSJob](RemotePBSJob.md)

Raises
------------
* ValueError: if a script has already been submitted within this
    [RemotePBSJob](RemotePBSJob.md) instance.
* TypeError: if `script` or `files` are not valid types.
* ValueError: if the files referened by `script` or `files` are not valid.

