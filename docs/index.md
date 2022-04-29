<p align="center"><a href="http://crimpl.readthedocs.io"><img src="./images/crimpl.png" alt="crimpl logo" width="300px" align="center"/></a></p>

<p align="center" style="text-align:center"><i>Connecting to Compute Resources made Simple(r)</i></p>

<pre align="center" style="text-align:center; font-family:monospace; margin: 30px">
  pip install crimpl
</pre>



[![badge](https://img.shields.io/badge/github-kecnry%2Fcrimpl-blue.svg)](https://github.com/kecnry/crimpl)
[![badge](https://img.shields.io/badge/pip-crimpl-lightgray.svg)](https://pypi.org/project/crimpl/)
![badge](https://img.shields.io/badge/python-3.6+-blue.svg)
[![badge](https://img.shields.io/badge/license-GPL3-blue.svg)](https://github.com/kecnry/crimpl/blob/master/LICENSE)
[![badge](https://travis-ci.com/kecnry/crimpl.svg?branch=master)](https://travis-ci.com/kecnry/crimpl)
[![badge](https://img.shields.io/codecov/c/github/kecnry/crimpl)](https://codecov.io/gh/kecnry/crimpl)
[![badge](https://readthedocs.org/projects/crimpl/badge/?version=latest)](https://crimpl.readthedocs.io/en/latest/?badge=latest)


**IMPORTANT**: **crimpl** is currently still under development, is not yet well-tested, and is subject to significant API changes.  Please keep posted until an official release is ready.

Read the [latest documentation on readthedocs](https://crimpl.readthedocs.io) or [browse the current documentation](./docs/index.md).


**crimpl** provides high-level python object-oriented interfaces to manage running scripts within conda environments on remote compute resources.

Each type of server implements a `run_script` which runs a given set of commands remotely on the server, showing the output, and waiting for completion, and `submit_script` which starts the script running on the server and detaches while allowing for monitoring its progress remotely.  They also each include a `s.check_output` for copying expected output files back to the local machine.

The configuration, options, and capabilities of each type of server are explored in more detail:

* [LocalThread](LocalThread.md)
* [RemoteThread](RemoteThread.md)
* [RemoteSlurm](RemoteSlurm.md)
* [RemotePBS](RemotePBS.md)
* [AWSEC2](AWSEC2.md)


## API Documentation

Local Thread:

* [LocalThreadServer](./api/LocalThreadServer.md)
* [LocalThreadJob](./api/LocalThreadJob.md)


RemoteThread:

* [RemoteThreadServer](./api/RemoteThreadServer.md)
* [RemoteThreadJob](./api/RemoteThreadJob.md)


Remote Slurm:

* [RemoteSlurmServer](./api/RemoteSlurmServer.md)
* [RemoteSlurmJob](./api/RemoteSlurmJob.md)


Remote PBS:

* [RemotePBSServer](./api/RemotePBSServer.md)
* [RemotePBSJob](./api/RemotePBSJob.md)


AWS EC2:

* [AWSEC2Server](./api/AWSEC2Server.md)
* [AWSEC2Job](./api/AWSEC2Job.md)





## Contributors

[Kyle Conroy](https://github.com/kecnry)

Contributions are welcome!  Feel free to file an issue or fork and create a pull-request.
