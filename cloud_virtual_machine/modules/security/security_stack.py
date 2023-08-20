import aws_cdk.aws_ssm as ssm
from aws_cdk import (

    aws_ec2 as ec2, NestedStack, CfnOutput, RemovalPolicy,
)
from constructs import Construct


class SecurityStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, whitelisted_peer: ec2.Peer, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.outer_perimeter_security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                                                vpc=vpc,
                                                                description="Allow ssh access to ec2 instances",
                                                                allow_all_outbound=True
                                                                )

        self.outer_perimeter_security_group.add_ingress_rule(whitelisted_peer, ec2.Port.tcp(22),
                                                             "allow ssh access from the world")
        self.outer_perimeter_security_group.add_ingress_rule(whitelisted_peer, ec2.Port.udp_range(60000, 61000),
                                                             "allow mosh access from the world")
        self.outer_perimeter_security_group.add_egress_rule(whitelisted_peer, ec2.Port.udp_range(60000, 60001),
                                                            "allow mosh access out to the world")

        CfnOutput(self, 'OuterPerimeterSecurityGroup',
                  description='SecurityGroup acting as first-line of defence from the outside world.',
                  value=self.outer_perimeter_security_group.security_group_id,
                  )
