# CloudVirtualMachine

CloudVirtualMachine (CVM) serves to allow one to easily provision cheap, stateless working EC2 instances on the AWS
cloud. Think of it as a [Terminal](https://fallout.fandom.com/wiki/Terminal).

## How to use

### Connect to Bastion host
Your instance is isolated and fronted by
a [Bastion](https://aws.amazon.com/blogs/security/controlling-network-access-to-ec2-instances-using-a-bastion-server/).
Therefore, to connect to your instance you need to jump via your Bastion. This is how to do it.

1. Send public SSH key to EC2.

[EC2 Instance Connect](https://aws.amazon.com/blogs/infrastructure-and-automation/securing-your-bastion-hosts-with-amazon-ec2-instance-connect/)
works by uploading a one-time SSH public key to the Bastion host, which will grant you access via your SSH client of
choice. After deployment, a pre-formatted CLI command with by outputted for you to paste into your console. It looks something like this: 

```
aws ec2-instance-connect send-ssh-public-key --instance-id i-xxxxxxxxxxxx --instance-os-user ec2-user --ssh-public-key file://C:\Users\whoever\CloudVirtualMachine\temp_key.pub --availability-zone eu-west-1a
```

2. Connect via SSH

Once your public SSH key has been sent to EC2, you can now connect using the SSH client of your choice. Similarly, a sample command is generated for you. For example: 

```
ssh -o "IdentitiesOnly=yes" -i C:\Users\whoever\CloudVirtualMachine\temp_key.pem ec2-user@ec2-34-000-000-19.eu-west-1.compute.amazonaws.com
```

### Jump to worker Instance

From your Bastion host, you can now jump to your worker Instance.
