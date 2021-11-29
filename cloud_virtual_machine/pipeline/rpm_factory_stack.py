from aws_cdk import (core as cdk, )

class RpmFactoryStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # TODO package RPM artifacts
        # Use this for now:
        # https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_arm64/amazon-ssm-agent.rpm
        # https://docs.aws.amazon.com/systems-manager/latest/userguide/agent-install-al2.html
        #
