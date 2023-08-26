#!/usr/bin/env python3
import os

from aws_cdk import (

    aws_ec2 as ec2,
    Environment, App, RemovalPolicy
)

from cloud_virtual_machine.cloud_terminal_stack import CloudTerminal

app = App()

default_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
africa_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='af-south-1')
euro_env = Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='eu-central-1')

peers = app.node.try_get_context("peers")
key_name = app.node.try_get_context("key_name")

CloudTerminal(app, "CloudTerminal", key_name=key_name,
              debug_mode=True,
              whitelisted_peer=ec2.Peer.prefix_list(peers),
              removal_policy=RemovalPolicy.DESTROY,
              env=default_env)

app.synth()
