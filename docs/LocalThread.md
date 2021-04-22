The Local Thread implementation allows submitting jobs on the local machine in a remote directory, with similar syntax and calling structures as other remote servers in crimpl.

# The Local Thread Server

To connect to a crimpl server running jobs in threads in a directory on the local machine:

```
import crimpl

s = crimpl.LocalThreadServer(directory='~/crimpl')

```

where `directory` will be created if it does not exit (but should preferably be empty) and available to the user with read and write permissions.  **crimpl** will create subdirectories for each job within this directory to try to avoid name conflicts, but any conflicts will overwrite existing files.

# Environment Setup

Setting up the necessary dependencies can be done within the job script itself (in which case it will be run within the scheduled job) or in advance in the root directory.  To run a script directly and wait for its output:

```
s.run_script(script)
```

By default this takes place in the 'default' conda environment if conda is installed on the remote machine, otherwise will run without a conda environment.  These defaults can be overridden by passing `conda_env` to `run_script` (a new environment is created if one with the same name does not yet exist).  For example:

```
s.run_script(["conda install condadeps -y",
              "pip install pipdeps"],
             conda_env='my_custom_env')
```

To force crimpl to not use conda even if it is installed, pass `conda_env=False`.

Alternatively, you could include all of these same instructions in the job script and they will be run in a detached thread before the job itself.

# Local Thread Jobs

To run computation jobs, create a [LocalThreadJob](./api/LocalThreadJob.md) instance attached to a [LocalThreadServer](./api/LocalThreadServer.md).

To create a new job, call [LocalThreadServer.create_job](./api/LocalThreadServer.create_job.md):

```
j = s.create_job(job_name='my-unique-jobname')
```

at which point you can run or submit scripts:

* [LocalThreadJob.run_script](./api/LocalThreadJob.run_script.md)
* [LocalThreadJob.submit_script](./api/RemotSlurmJob.submit_script.md)

Note that the Local Thread implementation does not accept `nprocs`.  To run in parallel, call `mpirun -np 4` (for example) directly in the script itself.

If not using the default conda environment, pass the same `conda_env` to `create_job` and the correct environment will automatically be activated before running the script.

Calling `j.submit_script` will then submit the job in a thread and set the `j.pid` of the running process.

```
j.submit_script(script, files=[...])
```

As a shorcut, [LocalThreadServer.submit_job](./api/LocalThreadServer.submit_job.md) combines both `s.create_job` and `sj.submit_script` into a single line.

# Retrieving an Existing Job

To retrieve the [LocalThreadJob](./api/LocalThreadJob.md) instance for an existing job on a server, call [LocalThreadServer.get_job](./api/LocalThreadServer.get_job.md):

```
j = crimpl.LocalThreadServer(...).get_job(job_name='my-unique-jobname')
```

If `job_name` was not provided while creating the job, it could be accessed via [LocalThreadJob.job_name](./api/LocalThreadJob.job_name.md) or [LocalThreadServer.existing_jobs](./api/LocalThreadServer.existing_jobs.md).


# Retrieving Results

To check the status of the job, call [LocalThreadJob.job_status](./api/LocalThreadJob.job_status.md):

```
print(j.job_status)
```

To wait in a loop until the job reaches a desired status, call [LocalThreadJob.wait_for_job_status](./api/LocalThreadJob.wait_for_job_status.md):

```
j.wait_for_job_status('complete')
```

To retrieve expected output files from the server directory, call [LocalThreadJob.check_output](./api/LocalThreadJob.check_output.md):

```
j.check_output(filename_on_server, local_filename)
```

where `filename_on_server` is the expected path(s) relative to the server working directory.
