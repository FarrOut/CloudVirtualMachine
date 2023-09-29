import aws_cdk as cdk
from aws_cdk import (
    NestedStack,
    aws_ec2 as ec2,
)
from constructs import Construct

from cloud_virtual_machine.components.networking_stack import NetworkingStack
from cloud_virtual_machine.components.security_stack import SecurityStack


class InfraStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, whitelisted_peer: ec2.Peer,
                 removal_policy: cdk.RemovalPolicy = cdk.RemovalPolicy.RETAIN, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # =====================
        # NETWORKING
        # =====================
        self.net = NetworkingStack(self, "NetworkingStack", removal_policy=removal_policy, )

        cdk.CfnOutput(self, 'VpcId',
                      description='Identifier for this VPC.',
                      value=self.net.vpc.vpc_id,
                      )

        # =====================
        # SECURITY
        # =====================
        self.sec = SecurityStack(self, "SecurityStack", vpc=self.net.vpc, whitelisted_peer=whitelisted_peer,
                                 removal_policy=removal_policy)
