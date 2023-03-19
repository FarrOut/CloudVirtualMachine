#!/usr/bin/env python3
import os

from aws_cdk import (

    aws_ec2 as ec2,
    Environment, App
)

# from cloud_virtual_machine.pipeline_stack import PipelineStack
from cloud_virtual_machine.infra_stack import InfraStack
from cloud_virtual_machine.terminal_stack import TerminalStack

# from cloud_virtual_machine.logging_stack import LoggingStack

app = App()

default_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
africa_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='af-south-1')
euro_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='eu-central-1')

# PipelineStack(app, "PipelineStack", env=default_env)

peers = app.node.try_get_context("peers")
key_name = app.node.try_get_context("key_name")

infra = InfraStack(app, "InfrastructureStack", whitelisted_peer=ec2.Peer.prefix_list(peers), env=default_env)
TerminalStack(app, "TerminalStack", vpc=infra.net.vpc, key_name=key_name,
              security_group=infra.sec.outer_perimeter_security_group,
              debug_mode=True,
              env=default_env)
# LoggingStack(app, "LoggingStack", env=euro_env)

app.synth()
