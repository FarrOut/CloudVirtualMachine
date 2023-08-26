from aws_cdk import (

    aws_ec2 as ec2, Stack, RemovalPolicy, Duration,
)
from constructs import Construct

from cloud_virtual_machine.components.infra_stack import InfraStack
from cloud_virtual_machine.components.terminal_stack import TerminalStack


class CloudTerminal(Stack):

    def __init__(self, scope: Construct, construct_id: str, whitelisted_peer: ec2.Peer, key_name: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN, debug_mode: bool = False, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        infra = InfraStack(self, "InfrastructureStack", whitelisted_peer=whitelisted_peer,
                           timeout=Duration.minutes(5), removal_policy=removal_policy, )

        TerminalStack(self, "TerminalStack", vpc=infra.net.vpc, key_name=key_name,
                      security_group=infra.sec.outer_perimeter_security_group,
                      debug_mode=debug_mode, timeout=Duration.minutes(15), )
