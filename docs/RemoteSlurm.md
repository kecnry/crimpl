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

This may often include setting up a virtual or anaconda environment and installing dependencies.  For example:

```
s.run_script(["python3 -m venv ~/tmp_venv",
              "source ~/tmp_venv/bin/activate",
              "python3 -m pip install mydependencies"])
```

In this case, just re-include the activation of the same virtual environment when submitting the job script.  Alternatively, you could include all of these same instructions in the job script and they would be run within the scheduler itself.

# Remote Slurm Jobs

To run computation jobs via the Slurm scheduler, create a [RemoteSlurmJob](./api/RemoteSlurmJob.md) instance attached to a [RemoteSlurmServer](./api/RemoteSlurmServer.md).

To create a new job, call [RemoteSlurmServer.create_job](./api/RemoteSlurmServer.create_job.md):

```
j = s.create_job(nprocs=8, job_name='my-unique-jobname')
```

at which point you can run or submit scripts:

* [RemoteSlurmJob.run_script](./api/RemoteSlurmJob.run_script.md)
* [RemoteSlurmJob.submit_script](./api/RemotSlurmJob.submit_script.md)

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

# Checking Status

To check the status of the job (currently just the output of `squeue`), call [RemoteSlurmJob.status](./api/RemoteSlurmJob.status.md).


# Retrieving Results

To retrieve expected output files from the server via scp, call [RemoteSlurmJob.check_output](./api/RemoteSlurmJob.check_output.md):

```
j.check_output(filename_on_server, local_filename)
```

where `filename_on_server` is the expected path relative to the remote working directory.
