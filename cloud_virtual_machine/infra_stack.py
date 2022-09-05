import aws_cdk as cdk
import aws_cdk.aws_ssm as ssm
from aws_cdk import (

    aws_ec2 as ec2,
)
from constructs import Construct


class InfraStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # =====================
        # NETWORKING
        # =====================
        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs=1,
                           )

        # Create a new SSM Parameter holding a StringList
        self.whitelisted_peers_parameter = ssm.StringListParameter(self, "WhitelistedPeers",
                                                                   description='IP address to be whitelisted and allowed to enter our perimeter.',
                                                                   string_list_value=[]
                                                                   )
        self.whitelisted_peers_parameter.apply_removal_policy(cdk.RemovalPolicy.RETAIN)
