from aws_cdk import (core as cdk,
aws_ec2 as ec2,
aws_secretsmanager as secretsmanager,
aws_s3_assets as assets,
aws_autoscaling as autoscaling,
aws_logs as logs,
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
# from pipeline_stage import WorkshopPipelineStage
import os

class LoggingStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

# View CloudFormation Logs in the Console
# https://aws.amazon.com/blogs/devops/view-cloudformation-logs-in-the-console/
        instance_log_group = logs.LogGroup(self, 'InstanceLogGroup',
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )        

        cdk.CfnOutput(self, 'InstanceLogGroupNameOutput',
            value=instance_log_group.log_group_name,
            description='Instance LogGroup Name',
            export_name='InstanceLogGroup',
        )
