import pytest
import crimpl

def test_remoteslurm():
    s = crimpl.RemoteSlurmServer(host='myserver', directory='~/blah')


if __name__ == '__main__':
    test_remoteslurm()
