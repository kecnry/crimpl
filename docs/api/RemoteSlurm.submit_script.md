### [RemoteSlurm](RemoteSlurm.md).submit_script (function)


```py

def submit_script(self, script, files=[], jobname=None, nprocs=4, walltime='2-00:00:00', mail_type='END,FAIL', mail_user=None, trial_run=False)

```



Submit a script to the server.

This will copy `script` (modified with the provided slurm options) and
`files` to the server and submit the script to the slurm scheduler.

Additional slurm customization (not included in the keyword arguments
listed below) can be included in the beginning of the script.

To check on any expected output files, call [RemoteSlurm.check_output](RemoteSlurm.check_output.md).

See [RemoteSlurm.run_script](RemoteSlurm.run_script.md) to run a script and wait for it to complete.

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
* `jobname` (string, optional, default=None): name of the job within slurm.
    Prepended to `script` as "#SBATCH -J jobname".
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
* (int): [RemoteSlurm.job_id](RemoteSlurm.job_id.md)

Raises
------------
* ValueError: if a script has already been submitted within this
    [RemoteSlurm](RemoteSlurm.md) instance.  To run another script, call [RemoteSlurm.release_job](RemoteSlurm.release_job.md)
    or create another [RemoteSlurm](RemoteSlurm.md) instance.
* TypeError: if `script` or `files` are not valid types.
* ValueError: if the files referened by `script` or `files` are not valid.

