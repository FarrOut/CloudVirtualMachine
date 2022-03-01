#!/usr/bin/env python3
import os
import socket

import aws_cdk as cdk
# from cloud_virtual_machine.pipeline_stack import PipelineStack
from aws_cdk import (
    aws_ec2 as ec2,
)

from cloud_virtual_machine.instance_stack import InstanceStack


# from cloud_virtual_machine.logging_stack import LoggingStack


def get_my_ip() -> str:
    hostname = socket.gethostname()
    print("Your Computer hostname is:" + hostname)

    ip = socket.gethostbyname(hostname)
    print("Your Computer IP Address is:" + ip)

    ipv6 = str(socket.getaddrinfo(hostname, None, socket.AF_INET6)[0][4][0])
    print("Your Computer IPv6 Address is:" + ipv6)

    return ipv6


app = cdk.App()

default_env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
rsa_env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='af-south-1')
euro_env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='eu-central-1')

# PipelineStack(app, "PipelineStack", env=default_env)

InstanceStack(app, "InstanceStack", env=default_env, whitelisted_peer=ec2.Peer.ipv6(get_my_ip() + '/32'))
# LoggingStack(app, "LoggingStack", env=euro_env)

app.synth()
