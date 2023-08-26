import aws_cdk.aws_ssm as ssm
from aws_cdk import (
    aws_logs as logs,
    aws_iam as iam,
    aws_ec2 as ec2, NestedStack, CfnOutput, RemovalPolicy,
)
from aws_cdk.aws_logs import RetentionDays
from constructs import Construct


class NetworkingStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # =====================
        # NETWORKING
        # =====================
        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs=1,
                           )

        log_group = logs.LogGroup(self, "VpcFlowLogGroup",
                                  removal_policy=removal_policy,
                                  retention=RetentionDays.ONE_WEEK,
                                  )

        vpc_flow_logs_role = iam.Role(self, "VpcFlowLogsRole",
                                      assumed_by=iam.ServicePrincipal("vpc-flow-logs.amazonaws.com")
                                      )

        flow_log = ec2.FlowLog(self, "FlowLog",
                               resource_type=ec2.FlowLogResourceType.from_vpc(self.vpc),
                               destination=ec2.FlowLogDestination.to_cloud_watch_logs(log_group, vpc_flow_logs_role),
                               )
        flow_log.apply_removal_policy(removal_policy)

        CfnOutput(self, 'VpcFlowLogGroupName',
                  description='Name of LogGroup storing FlowLogs for this VPC.',
                  value=log_group.log_group_name,
                  )
        CfnOutput(self, 'VpcFlowLogGroupArn',
                  description='ARN of LogGroup storing FlowLogs for this VPC.',
                  value=log_group.log_group_arn,
                  )

        # # Create a new SSM Parameter holding a StringList
        # self.whitelisted_peers_parameter = ssm.StringListParameter(self, "WhitelistedPeers",
        #                                                            description='IP address to be whitelisted and allowed to enter our perimeter.',
        #                                                            string_list_value=[]
        #                                                            )
        # self.whitelisted_peers_parameter.apply_removal_policy(RemovalPolicy.RETAIN)

        CfnOutput(self, 'VpcId',
                  description='Identifier for this VPC.',
                  value=self.vpc.vpc_id,
                  )

        CfnOutput(self, 'Vpc',
                  description='Arn of this VPC.',
                  value=self.vpc.vpc_arn,
                  )

        CfnOutput(self, 'PrivateSubnets',
                  description='List of private subnets in this VPC.',
                  value=str([s.subnet_id for s in self.vpc.private_subnets]),
                  )

        CfnOutput(self, 'IsolatedSubnets',
                  description='List of isolated subnets in this VPC.',
                  value=str([s.subnet_id for s in self.vpc.isolated_subnets]),
                  )

        CfnOutput(self, 'PublicSubnets',
                  description='List of public subnets in this VPC.',
                  value=str([s.subnet_id for s in self.vpc.public_subnets]),
                  )

        CfnOutput(self, 'AvailabilityZones',
                  description='AZs for this VPC.',
                  value=str(self.vpc.availability_zones),
                  )
