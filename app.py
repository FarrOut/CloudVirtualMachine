#!/usr/bin/env python3
import os

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from cloud_virtual_machine.pipeline.pipeline_stack import PipelineStack
from cloud_virtual_machine.pipeline.rpm_factory_stack import RpmFactoryStack
from cloud_virtual_machine.instance_stack import InstanceStack
from cloud_virtual_machine.logging_stack import LoggingStack

app = core.App()

default_env = core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
rsa_env = core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='af-south-1')
euro_env = core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region='eu-central-1')

PipelineStack(app, "PipelineStack", env=default_env)
RpmFactoryStack(app, "PackageFactoryStack", env=default_env)
InstanceStack(app, "InstanceStack", env=euro_env)
LoggingStack(app, "LoggingStack", env=euro_env)

app.synth()
