#!/usr/bin/env python3
import os

from aws_cdk import (

    aws_ec2 as ec2,
    Environment, App
)

# from cloud_virtual_machine.pipeline_stack import PipelineStack
from cloud_virtual_machine.terminal_stack import TerminalStack

# from cloud_virtual_machine.logging_stack import LoggingStack

app = App()

default_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
rsa_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='af-south-1')
euro_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='eu-central-1')

# PipelineStack(app, "PipelineStack", env=default_env)
TerminalStack(app, "TerminalStack", whitelisted_peer=ec2.Peer.prefix_list(), env=default_env)
# LoggingStack(app, "LoggingStack", env=euro_env)

app.synth()
