from aws_cdk import core as cdk

from cloud_virtual_machine.pipeline.rpm_factory_stack import RpmFactoryStack


class PackageFactoryStage(cdk.Stage):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        rpm_factory_stack = RpmFactoryStack(self, 'RpmFactoryStack')
