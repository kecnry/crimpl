# crimpl

<p align="center" style="text-align:center"><i>Connecting to Compute Resources made Simple(r)</i></p>

<!-- <pre align="center" style="text-align:center; font-family:monospace; margin: 30px">
  pip install crimpl
</pre> -->



[![badge](https://img.shields.io/badge/github-kecnry%2Fcrimpl-blue.svg)](https://github.com/kecnry/crimpl)
[![badge](https://img.shields.io/badge/pip-crimpl-lightgray.svg)](https://pypi.org/project/crimpl/)
![badge](https://img.shields.io/badge/python-3.6+-blue.svg)
[![badge](https://img.shields.io/badge/license-GPL3-blue.svg)](https://github.com/kecnry/crimpl/blob/master/LICENSE)
[![badge](https://travis-ci.com/kecnry/crimpl.svg?branch=master)](https://travis-ci.com/kecnry/crimpl)
[![badge](https://img.shields.io/codecov/c/github/kecnry/crimpl)](https://codecov.io/gh/kecnry/crimpl)
[![badge](https://readthedocs.org/projects/crimpl/badge/?version=latest)](https://crimpl.readthedocs.io/en/latest/?badge=latest)


**IMPORTANT**: **crimpl** is currently still under development, is not yet well-tested, and is subject to significant API changes.  Please keep posted until an official release is ready.

Read the [latest documentation on readthedocs](https://crimpl.readthedocs.io) or [browse the current documentation](./docs/index.md).


**crimpl** provides high-level python object-oriented interfaces to managing running scripts on remote compute resources.

Each type of server implements a `s.run_script` which runs a given set of commands remotely on the server, showing the output, and waiting for completion, and `s.submit_script` which starts the script running on the server and detaches while allowing for monitoring its progress remotely.  They also each include a `s.check_output` for copying expected output files back to the local machine.

The configuration, options, and capabilities of each type of server are explored in more detail below.

## Remote Slurm


### Setup & Configuration

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

## Environment Setup

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

## Submitting Scripts

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

## Checking Status

To check the status of the job (currently just the output of `squeue`), call `s.job_status`.

Note that only one job can be submitted via `s.submit_script` per instance of `RemoteSlurm`.  To submit multiple jobs, create another `RemoteSlurm` instance, or disable tracking of a previously submitted script by calling `s.release_job()`.


## Retrieving Results

To retrieve expected output files from the server via scp, all:

```
s.check_output(filename_on_server, local_filename)
```

where `filename_on_server` is the expected path relative to the remote working directory.

## AWS EC2

The AWS EC2 implementation relies heavily upon [BOTO3](https://boto3.readthedocs.io/).  For more advanced customization, consider using BOTO3 directly.  **crimpl** provides a high-level simplified interface to starting new or existing EC2 instances and submitting a script (including with any necessary installation/setup instructions).

### Setup & Configuration

* Create or log into an AWS account.  Make sure billing is set up.  Note that using the resources below will be billed to your account.  Make sure to research pricing rates in advance.
* [Install AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
* [AWS Management Console > IAM](https://console.aws.amazon.com/iam/home#/users): create new user with "Programmatic Access" but no "AWS Management Console Access", add to new or existing group with "AmazonEC2FullAccess" permissions.
* Call `aws configure`:
  * paste access key and secret from created IAM account
  * set appropriate zone (i.e. "us-east-1" **not** "us-east-1a")
* [AWS Management Console > EC2 > Key Pairs](https://console.aws.amazon.com/ec2/v2/home#KeyPairs:): create or download existing key-pair.  Its name in AWS will be referred to below as `KeyName` and its path on your local machine as `KeyFile`.
* [AWS Management Console > VPC > Subnets Management](https://console.aws.amazon.com/vpc/home#subnets:): create or copy an existing `SubnetId`.
* [AWS Management Console > VPC > Security Groups](https://console.aws.amazon.com/vpc/home#securityGroups:): create new security group.
  * name and give any description
  * choose scope: VPC.
  * set Inbound and Outbound rules to All TCP and SSH with destination "anywhere" (or more restrictive if you'd like)
  * note `SecurityGroupId`.

```
import crimpl

config = crimpl.AWSEC2_Config(KeyFile="...",
                              KeyName="...",
                              SubnetId="...",
                              SecurityGroupId="...")

```

(**NOT YET IMPLEMENTED** - for now you'll have to create and pass this `config` object each time) to save these settings to a file in your `~/.crimpl` directory (**warning**: will be saved in plain text) and no longer need to worry about the config:

```
config.save('my_ec2_configname')
```

If only one config has been saved for `AWS_EC2` then the configuration will be loaded automatically:

```
s = crimpl.AWSEC2.new(...)
```

Otherwise, you'll just need to pass the name provided when saving:

```
s = crimpl.AWSEC2.new(config='my_ec2_configname', ...)
```


If no saved configurations exist, you will need to create the `config` object and pass it anytime you create a new server instance (use this option if you don't want to store any security details).

```
s = crimpl.AWSEC2.new(config=config, ...)
```

### Managing Server State

A new server can be launched by calling (see above for configuration requirements):

```
s = crimpl.AWSEC2.new(nprocs=4)
```

or a previously created server can be retrieved by referring to its `instanceId` (if you may want to close python and re-connect later, it is very useful to call `print(s.instanceId)` at some point, otherwise you must check the [AWS EC2 Console](https://console.aws.amazon.com/ec2/v2/home#Instances:) to get the `instanceId`):

```
sr = crimpl.AWSEC2(s.instanceId)
```

the current state can be accessed via:

```
print(s.state)
```

and the server can be started, stopped, or terminated via `s.start()`, `s.stop()`, and `s.terminate()`, respectively.

Note that a stopped server will not charge for CPU usage, but will charge (albeit less) for storage.  However, a stopped server can be restarted quicker than re-installing on a brand new instance.

## Submitting Scripts

`AWSEC2` instances are designed to be built for a single job or multiple jobs submitted in serial (to save time during installation, no job queueing system is installed and jobs are run to use all available resources).

To submit a job, pass a _shell script_ (as either a filename or as a list of commands) as well as any additional files that need to be copied to the server:

```
s.submit_script(script, files=[...])
```

Note that any required installation or setup steps should be included in this shell script (or they can be run separately while waiting for output via `s.run_script`).  To run a python code, for example, you may do something like the following:

```
s.submit_script(script=['curl -O https://bootstrap.pypa.io/get-pip.py',
                        'python3 get-pip.py --user',
                        'pip install my_dependencies',
                        'python3 myscript.py'],
                files=['myscript.py'])
```
## Retrieving Results

To retrieve expected output files from the server via scp, call:

```
s.check_output(filename_on_server, local_filename)
```
