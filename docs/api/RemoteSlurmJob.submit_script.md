### [RemoteSlurmJob](RemoteSlurmJob.md).submit_script (function)


```py

def submit_script(self, script, files=[], job_name=None, nprocs=4, walltime='2-00:00:00', mail_type='END,FAIL', mail_user=None, trial_run=False)

```



Submit a script to the server.

This will copy `script` (modified with the provided slurm options) and
`files` to [RemoteSlurmJob.remote_directory](RemoteSlurmJob.remote_directory.md) on the remote server and
submit the script to the slurm scheduler.  To check on its status,
see [RemoteSlurmJob.status](RemoteSlurmJob.status.md).

Additional slurm customization (not included in the keyword arguments
listed below) can be included in the beginning of the script.

To check on any expected output files, call [RemoteSlurmJob.check_output](RemoteSlurmJob.check_output.md).

See [RemoteSlurmJob.run_script](RemoteSlurmJob.run_script.md) to run a script and wait for it to complete.

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
* `job_name` (string, optional, default=None): name of the job within slurm.
    Prepended to `script` as "#SBATCH -J jobname".  Defaults to
    [RemoteSlurmJob.job_name](RemoteSlurmJob.job_name.md).
* `nprocs` (int, optional, default=4): number of processors to run the
    job.  Prepended to `script` as "#SBATCH -n nprocs".
* `walltime` (string, optional, default='2-00:00:00'): maximum walltime
    to schedule the job.  Prepended to `script` as "#SBATCH -t walltime".
* `mail_type` (string, optional, default='END,FAIL'): conditions to notify
    by email to `mail_user`.  Prepended to `script` as "#SBATCH --mail_user=mail_user".
* `mail_user` (string, optional, default=None): email to send notifications.
    Prepended to `script` as "#SBATCH --mail_user=mail_user"
* `trial_run` (bool, optional, default=False): if True, the commands
    that would be sent to the server are returned but not executed.

Returns
------------
* (int): [RemoteSlurmJob.slurm_id](RemoteSlurmJob.slurm_id.md)

Raises
------------
* ValueError: if a script has already been submitted within this
    [RemoteSlurmJob](RemoteSlurmJob.md) instance.  To run another script, call [RemoteSlurmJob.release_job](RemoteSlurmJob.release_job.md)
    or create another [RemoteSlurmJob](RemoteSlurmJob.md) instance.
* TypeError: if `script` or `files` are not valid types.
* ValueError: if the files referened by `script` or `files` are not valid.

