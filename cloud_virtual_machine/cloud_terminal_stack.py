from aws_cdk import (

    Duration,
    Environment,
    Stack,
    aws_ec2 as ec2,
    aws_logs as logs, CfnOutput, RemovalPolicy,
)
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy
from aws_cdk.aws_s3 import Bucket
from constructs import Construct
from cloud_virtual_machine.modules.terminal_stack import TerminalStack

from cloud_virtual_machine.stacks.infra_stack import InfraStack


class CloudTerminalStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,  whitelisted_peer: ec2.Peer,             key_name: str, debug_mode: bool, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        infra = InfraStack(self, "InfrastructureStack", whitelisted_peer=whitelisted_peer)

        terminal = TerminalStack(self, "TerminalStack", vpc=infra.net.vpc, key_name=key_name,
              security_group=infra.sec.outer_perimeter_security_group,
              debug_mode=debug_mode,)
        # terminal.node.default_child.cfn_options.creation_timeout = Duration.minutes(5)
        # terminal.node.default_child.cfn_options.timeout_in_minutes = 5