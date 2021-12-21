import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (
    aws_logs as logs,
)

class LoggingStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
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
