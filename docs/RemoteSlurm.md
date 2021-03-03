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

* Configure server options:

```
import crimpl

config = crimpl.RemoteSlurmConfig(host='myserver',
                                  directory='~/my_crimpl_jobs')
```

where `directory` is an existing (preferably empty) directory, available to the user with read and write permissions.  **crimpl** will create subdirectories for each job within this directory to try to avoid name conflicts, but any conflicts will overwrite existing files.

(**NOT YET IMPLEMENTED** - for now you'll have to create and pass this `config` object each time) to save these settings to a file in your `~/.crimpl` directory (**warning**: will be saved in plain text) and no longer need to worry about the config:

```
config.save('my_remoteslurm_configname')
```

If only one config has been saved for `RemoteSlurm` then the configuration will be loaded automatically:

```
s = crimpl.RemoteSlurm.new(...)
```

Otherwise, you'll just need to pass the name provided when saving:

```
s = crimpl.RemoteSlurm.new(config='my_remoteslurm_configname', ...)
```

If no saved configurations exist, you will need to create the `config` object and pass it anytime you create a new server instance.

```
s = crimpl.RemoteSlurm(config=config, ...)
```

# Environment Setup

Setting up the necessary dependencies can be done within the job script itself (in which case it will be run within the scheduled job) or in advance.  To run a script directly and wait for its output:

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

# Submitting Scripts

Submitting a script will edit the input script into a "sbatch" file to submit to the slurm scheduler.  `s.submit_script` accepts the following keyword arguments as options for the job:
* `jobname`
* `nprocs`
* `walltime`
* `mail_type`
* `mail_user`

Any more advanced slurm configuration can be included directly in the input `script` itself.

Calling `s.submit_script` will then submit the job to the remote scheduler and set the `s.job_id` returned by slurm.

```
s.submit_script(script, files=[...])
```

# Checking Status

To check the status of the job (currently just the output of `squeue`), call `s.job_status`.

Note that only one job can be submitted via `s.submit_script` per instance of `RemoteSlurm`.  To submit multiple jobs, create another `RemoteSlurm` instance, or disable tracking of a previously submitted script by calling `s.release_job()`.


# Retrieving Results

To retrieve expected output files from the server via scp, all:

```
s.check_output(filename_on_server, local_filename)
```

where `filename_on_server` is the expected path relative to the remote working directory.
