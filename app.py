#!/usr/bin/env python3
import os

from aws_cdk import (

    Duration,
    aws_ec2 as ec2,
    Environment, App
)
from cloud_virtual_machine.cloud_terminal_stack import CloudTerminalStack


# from cloud_virtual_machine.logging_stack import LoggingStack

app = App()

default_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
africa_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='af-south-1')
euro_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='eu-central-1')

# PipelineStack(app, "PipelineStack", env=default_env)

peers = app.node.try_get_context("peers")
key_name = app.node.try_get_context("key_name")


CloudTerminalStack(app, "CloudTerminalStack",  key_name=key_name,
                   whitelisted_peer=ec2.Peer.prefix_list(peers),
              debug_mode=True,
              env=default_env)



# LoggingStack(app, "LoggingStack", env=euro_env)

app.synth()
