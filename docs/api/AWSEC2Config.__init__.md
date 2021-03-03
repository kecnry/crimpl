### [AWSEC2Config](AWSEC2Config.md).__init__ (function)


```py

def __init__(self, KeyFile=None, KeyName=None, SubnetId=None, SecurityGroupId=None)

```



ec2 = boto3.resource('ec2')

# create a file to store the key locally
outfile = open('ec2-keypair.pem','w')

# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
print(KeyPairOut)
outfile.write(KeyPairOut)
# may also need to chmod to 400

