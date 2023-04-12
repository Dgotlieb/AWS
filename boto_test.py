import boto3

# Create a session object with your AWS secret access key
session = boto3.Session(
    aws_access_key_id='XXXXXXXXXXXX',
    aws_secret_access_key='XXXXXXXXXXXXX'
)

# Create an EC2 client using the session object
ec2 = session.client('ec2')

# create a file to store the key locally
key_file = open('ec2-keypair.pem', 'w')

# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

# capture the key and store it in a file
KeyPairOut = str(key_pair['KeyMaterial'])
# print(KeyPairOut)
key_file.write(KeyPairOut)
key_file.close()


# create a new security group
security_group = ec2.create_security_group(
    GroupName='my-security-group',
    Description='My security group'
)

# authorize inbound traffic on port 22
ec2.authorize_security_group_ingress(
    GroupId=security_group['GroupId'],
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)


# Create a new EC2 instance
instance = ec2.run_instances(
    ImageId='ami-0ec7f9846da6b0f61', # Enter the ID of the AMI you want to use
    InstanceType='t2.micro', # Enter the instance type you want to use
    MinCount=1,
    MaxCount=1,
    KeyName='ec2-keypair',
    SecurityGroupIds=[security_group['GroupId']]
)

# Get the instance ID
instance_id = instance['Instances'][0]['InstanceId']

# Wait for the instance to be running
ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])

public_ip = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]['PublicIpAddress']

print('Instance is ready, to connect, please type the below commands in a terminal:')
print('chmod 400 ec2-keypair.pem')
print(f"ssh ubuntu@{public_ip} -i ec2-keypair.pem")
