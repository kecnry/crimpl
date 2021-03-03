from nose.tools import assert_raises

import crimpl

def test_remoteslurm():
    s = crimpl.RemoteSlurm(host='myserver', directory='~/blah')

def test_awsec2():
    c = crimpl.AWSEC2Config()
    # TODO: figure out how to test this remotely
    #s = crimpl.AWSEC2.new(c)


if __name__ == '__main__':
    test_remoteslurm()
    test_awsec2()
