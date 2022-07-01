#!/usr/bin/env python3
import os
import socket
from typing import List

import aws_cdk as cdk
# from cloud_virtual_machine.pipeline_stack import PipelineStack
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ssm as ssm,
)

# from cloud_virtual_machine.logging_stack import LoggingStack
from aws_cdk.aws_ssm import StringListParameter

from cloud_virtual_machine.security import ssh_key_handler
from cloud_virtual_machine.terminal_stack import TerminalStack
from cloud_virtual_machine.infra_stack import InfraStack


# TODO automatically detect local IP address
def get_my_ip() -> str:
    hostname = socket.gethostname()
    print("Your Computer hostname is:" + hostname)

    ip = socket.gethostbyname(hostname)
    print("Your Computer IP Address is:" + ip)

    ipv6 = str(socket.getaddrinfo(hostname, None, socket.AF_INET6)[0][4][0])
    print("Your Computer IPv6 Address is:" + ipv6)

    return ipv6


def get_whitelisted_peers(whitelisted_peers: StringListParameter) -> List[str]:
    return whitelisted_peers.string_list_value


app = cdk.App()

default_env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
rsa_env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='af-south-1')
euro_env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='eu-central-1')
the_env = rsa_env

# PipelineStack(app, "PipelineStack", env=default_env)

infra = InfraStack(app, "InfrastructureStack", env=the_env)

whitelisted_peers = get_whitelisted_peers(infra.whitelisted_peers_parameter)

TerminalStack(app, "TerminalStack", env=the_env, vpc=infra.vpc, ssh_public_key_path=ssh_key_handler.generate_key_pair(),
              whitelisted_peers=whitelisted_peers, )
# LoggingStack(app, "LoggingStack", env=euro_env)


app.synth()
