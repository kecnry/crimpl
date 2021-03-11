The AWS EC2 implementation relies heavily upon [BOTO3](https://boto3.readthedocs.io/).  For more advanced customization, consider using BOTO3 directly.  **crimpl** provides a high-level simplified interface to starting new or existing EC2 instances and submitting a script (including with any necessary installation/setup instructions).

# Setup & Configuration

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

# The AWS EC2 Server

With this information, you can now initialize a new [AWSEC2Server](./api/AWSEC2Server.md) instance.

```
import crimpl

s = crimpl.AWSEC2Server.new(server_name='my-aws-server'
                            volumeSize=8,
                            KeyFile="...",
                            KeyName="...",
                            SubnetId="...",
                            SecurityGroupId="...")

```

This creates an AWS EBS volume in your account at the specified size.  This volume will be persistent until you destroy it and will accrue charges starting as soon as the first EC2 instance of a server or job is started and the volume initialized.  The server object does allow initializing an EC2 instance with 1 server that mounts the volume, which is useful for running virtual environment installation script (note that the OS root volume itself will not be persistent between the server and job EC2 instances) or copying large files.

* [AWSEC2Server.start](./api/AWSEC2Server.start.md)
* [AWSEC2Server.stop](./api/AWSEC2Server.stop.md)
* [AWSEC2Server.terminate](./api/AWSEC2Server.terminate.md)
* [AWSEC2Server.state](./api/AWSEC2Server.state.md)
* [AWSEC2Server.delete_volume](./api/AWSEC2Server.delete_volume.md)
* [AWSEC2Server.run_script](./api/AWSEC2Server.run_script.md)

# Retrieving an Existing Server Instance

An existing [AWSEC2Server](./api/AWSEC2Server.md) instance can be retrieved (so long as the volume hasn't been manually deleted), by passing the provided `server_name` to [AWSEC2Server.\_\_init\_\_](./api/AWSEC2Server.__init__.md):

```
s = crimpl.AWSEC2Server(server_name='my-aws-server',
                        KeyFile="...",
                        KeyName="...",
                        SubnetId="...",
                        SecurityGroupId="...")
```

If `server_name` was not provided when creating the original instance, the generated name could be accessed with [AWSEC2Server.server_name](./api/AWSEC2Server.server_name.md).  If unknown, all existing volumes managed by **crimpl** can be listed with [crimpl.list_awsec2_volumes](./api/crimpl.list_awsec2_volumes.md) (where the `server_name` will show in the returned dictionary).

# The AWS EC2 Job Instance

To run computation jobs with more resources, create an [AWSEC2Job](./api/AWSEC2Job.md) instance attached to an [AWSEC2Server](./api/AWSEC2Server.md).  Once started, the resulting EC2 instance will be initialized with the requested number of processors (rounded up to the next available configuration) and with access to the same file volume as the server instance.

To create a new job, call [AWSEC2Server.create_job](./api/AWSEC2Server.create_job.md):

```
j = s.create_job(nprocs=8, job_name='my-unique-jobname')
```

Similarly, you can access and change the state of the underlying EC2 instance:

* [AWSEC2Job.start](./api/AWSEC2Job.start.md)
* [AWSEC2Job.stop](./api/AWSEC2Job.stop.md)
* [AWSEC2Job.terminate](./api/AWSEC2Job.terminate.md)
* [AWSEC2Job.state](./api/AWSEC2Job.state.md)

and can also run or submit scripts:

* [AWSEC2Job.run_script](./api/AWSEC2Job.run_script.md)
* [AWSEC2Job.submit_script](./api/AWSEC2Job.submit_script.md)

Note that charges are being accrued per CPU-second, so it can be costly to leave a large job EC2 instance running longer than necessary.

To see all running EC2 instances on your AWS account, check the [AWS EC2 Console](https://console.aws.amazon.com/ec2/v2/home#Instances:) or continue reading below to access through **crimpl**.

# Submitting Scripts

To submit a job, pass a _shell script_ (as either a filename or as a list of commands) as well as any additional files that need to be copied to the server via [AWSEC2Job.submit_script](./api/AWSEC2Job.submit_script.md):

```
j.submit_script(script, files=[...])
```

Note that any required installation or setup steps should be included in this shell script (or they can be run separately while waiting for output via `s.run_script`).  To run a python code, for example, you may do something like the following:

```
j.submit_script(script=['curl -O https://bootstrap.pypa.io/get-pip.py',
                        'python3 get-pip.py --user',
                        'pip install my_dependencies',
                        'python3 myscript.py'],
                files=['myscript.py'])
```


**COMING SOON**: If the setup script may take a while, it might make more financial sense to run that in advance from the 1-processor server EC2 instance.  This will not work quite yet as only the local file system is persistent between instances.  In the future, there will hopefully be a cleaner way to create local virtual or conda environments which are also persistent.

# Retrieving an Existing Job

To retrieve the [AWSEC2Job](./api/AWSEC2Job.md) instance for an existing job on an active server, call [AWSEC2Server.get_job](./api/AWSEC2Server.get_job.md):

```
j = crimpl.AWSEC2Server(...).get_job(job_name='my-unique-jobname')
```

If `job_name` was not provided while creating the job, it could be accessed via [AWSEC2Job.job_name](./api/AWSEC2Job.job_name.md) or [AWSEC2Server.existing_jobs](./api/AWSEC2Server.existing_jobs.md).

# Retrieving Results

To check on the status of a submitted job, call [AWSEC2Job.job_status](./api/AWSEC2Job.job_status.md).

To retrieve expected output files from the server via scp, call [AWSEC2Job.check_output](./api/AWSEC2Job.check_output.md):

```
j.check_output(filename_on_server, local_filename)
```
where `filename_on_server` is the expected path(s) relative to the remote working directory.


# Checking and Managing AWS Resources

It is most convenient to manage the state of EC2 instances and volumes from the [AWSEC2Server](./api/AWSEC2Server.md) and [AWSEC2Job](./api/AWSEC2Job.md) methods themselves.  However, top-level functions also exist to list all active instances and volumes within EC2 that are managed by **crimpl**.

* [list_awsec2_instances](./api/crimpl.list_awsec2_instances.md)
* [list_awsec2_volumes](./api/crimpl.list_awsec2_volumes.md)

If an instance or volume is running that is no longer needed, they can be manually terminated/deleted via:

* [terminate_awsec2_instance](./api/crimpl.terminate_awsec2_instance.md)
* [delete_awsec2_volume](./api/crimpl.delete_awsec2_volume.md)

Or all instances/volumes managed by crimpl can be terminated/deleted at once:

* [terminate_all_awsec2_instances](./api/crimpl.terminate_all_awsec2_instances.md)
* [delete_all_awsec2_volumes](./api/crimpl.delete_all_awsec2_volumes.md)

And it never hurts to check the online AWS dashboard to make sure that there are no unexpected running services that could result in charges:

* [AWS EC2 Instances Dashboard](https://console.aws.amazon.com/ec2/v2/home#Instances:)
* [AWS EC2 Volumes Dashboard](https://console.aws.amazon.com/ec2/v2/home#Volumes:sort=desc:createTime)
