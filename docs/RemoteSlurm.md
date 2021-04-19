The Remote Slurm implementation allows submitting jobs to a SLURM scheduler on a remote machine.

# Setup & Configuration

* Make sure you have passwordless login available to `host`.  Preferably setup something like the following in `~/.ssh/config`:

```
Host myserver
    HostName myserver_ip
    IdentityFile path_to_private_key
    User myusername
```

Otherwise, all instances of `host` below should include the username (i.e. `myusername@myserver_ip`).

# The Remote Slurm Server

To connect to a remote server running a Slurm job scheduler:

```
import crimpl

s = crimpl.RemoteSlurmServer(host='myserver',
                             directory='~/my_crimpl_jobs')

```

where `directory` will be created if it does not exit (but should preferably be empty) and available to the user with read and write permissions.  **crimpl** will create subdirectories for each job within this directory to try to avoid name conflicts, but any conflicts will overwrite existing files.

# Environment Setup

Setting up the necessary dependencies can be done within the job script itself (in which case it will be run within the scheduled job) or in advance in the root directory.  To run a script directly and wait for its output:

```
s.run_script(script)
```

By default this takes place in the 'default' conda environment, but can be overridden by passing `conda_env` to `run_script` (a new environment is created if one with the same name does not yet exist).  For example:

```
s.run_script(["conda install condadeps -y",
              "pip install pipdeps"],
             conda_env='my_custom_env')
```

Alternatively, you could include all of these same instructions in the job script and they would be run within the scheduler itself.

# Remote Slurm Jobs

To run computation jobs via the Slurm scheduler, create a [RemoteSlurmJob](./api/RemoteSlurmJob.md) instance attached to a [RemoteSlurmServer](./api/RemoteSlurmServer.md).

To create a new job, call [RemoteSlurmServer.create_job](./api/RemoteSlurmServer.create_job.md):

```
j = s.create_job(nprocs=8, job_name='my-unique-jobname')
```

at which point you can run or submit scripts:

* [RemoteSlurmJob.run_script](./api/RemoteSlurmJob.run_script.md)
* [RemoteSlurmJob.submit_script](./api/RemotSlurmJob.submit_script.md)

If not using the default conda environment, pass the same `conda_env` to `create_job` and the correct environment will automatically be activated before running the script.

Submitting a script will edit the input script into a "sbatch" file to submit to the slurm scheduler.  `j.submit_script` accepts the following keyword arguments as options for the job:

* `job_name`
* `nprocs`
* `walltime`
* `mail_type`
* `mail_user`


Any more advanced slurm configuration can be included directly in the input `script` itself.

Calling `j.submit_script` will then submit the job to the remote scheduler and set the `j.job_id` returned by slurm.

```
j.submit_script(script, files=[...])
```

As a shorcut, [RemoteSlurmServer.submit_job](./api/RemoteSlurmServer.submit_job.md) combines both `s.create_job` and `sj.submit_script` into a single line.

# Retrieving an Existing Job

To retrieve the [RemoteSlurmJob](./api/RemoteSlurmJob.md) instance for an existing job on a server, call [RemoteSlurmServer.get_job](./api/RemoteSlurmServer.get_job.md):

```
j = crimpl.RemoteSlurmServer(...).get_job(job_name='my-unique-jobname')
```

If `job_name` was not provided while creating the job, it could be accessed via [RemoteSlurmJob.job_name](./api/RemoteSlurmJob.job_name.md) or [RemoteSlurmServer.existing_jobs](./api/RemoteSlurmServer.existing_jobs.md).


# Retrieving Results

To check the status of the job, call [RemoteSlurmJob.job_status](./api/RemoteSlurmJob.job_status.md):

```
print(j.job_status)
```

To wait in a loop until the job reaches a desired status, call [RemoteSlurmJob.wait_for_job_status](./api/RemoteSlurmJob.wait_for_job_status.md):

```
j.wait_for_job_status('complete')
```

To retrieve expected output files from the server via scp, call [RemoteSlurmJob.check_output](./api/RemoteSlurmJob.check_output.md):

```
j.check_output(filename_on_server, local_filename)
```

where `filename_on_server` is the expected path(s) relative to the remote working directory.
