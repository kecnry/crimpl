### [AWSEC2Job](AWSEC2Job.md).submit_script (function)


```py

def submit_script(self, script, files=[], terminate_on_complete=True, wait_for_job_status=False, trial_run=False)

```



Submit a script to the server.

This will call &lt;AWSEC2Job.start&gt; and wait for
the server to intialize if it is not already running.  Once running,
`script` and `files` are copied to the server, and `script` is executed
in a screen session at which point this method will return.

To check on any expected output files, call &lt;AWSEC2Job.check_output&gt;.

See &lt;AWSEC2Job.run_script&gt; to run a script and wait for it to complete.

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
* `terminate_on_complete` (bool, optional, default=True): whether to terminate
    the EC2 instance once `script` has completed.  This is useful for
    long jobs where you may not immediately be able to pull the results
    to minimize costs.  In this case, the &lt;AWSEC2Job.server&gt; EC2 instance
    will be restarted when calling &lt;AWSEC2Job.check_output&gt; with access
    to the same storage volume.
* `wait_for_job_status` (bool or string or list, optional, default=False):
    Whether to wait for a specific job_status.  If True, will default to
    'complete'.  See also &lt;AWSEC2Job.wait_for_job_status&gt;.
* `trial_run` (bool, optional, default=False): if True, the commands
    that would be sent to the server are returned but not executed
    (and the server is not started automatically - so these may include
    an [ip](ip.md) placeholder).


Returns
------------
* &lt;AWSEC2Job&gt;

Raises
------------
* TypeError: if `script` or `files` are not valid types.
* ValueError: if the files referened by `script` or `files` are not valid.

