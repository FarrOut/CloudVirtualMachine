#!/usr/bin/env python3
import os

import aws_cdk as cdk

# from cloud_virtual_machine.pipeline_stack import PipelineStack
from cloud_virtual_machine.instance_stack import InstanceStack
# from cloud_virtual_machine.logging_stack import LoggingStack

app = cdk.App()

default_env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
rsa_env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='af-south-1')
euro_env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='eu-central-1')

# PipelineStack(app, "PipelineStack", env=default_env)
InstanceStack(app, "InstanceStack", env=default_env)
# LoggingStack(app, "LoggingStack", env=euro_env)

app.synth()
