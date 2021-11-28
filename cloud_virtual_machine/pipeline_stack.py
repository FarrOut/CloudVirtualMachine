import logging

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk import (core as cdk,
                     aws_ec2 as ec2,
                     pipelines,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as cpactions,
                     aws_secretsmanager,
                     )
from aws_cdk.core import CfnOutput, SecretValue
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
import boto3, json

secretsmanager = boto3.client('secretsmanager')


# from pipeline_stage import WorkshopPipelineStage


class PipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        logger = logging.getLogger()

        connection_secret = aws_secretsmanager.Secret.from_secret_name_v2(self, "GitHubConnectionSecret",
                                                                          'GitHub/FarrOut/connection')

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Client.get_secret_value
        connection_secret_value = json.loads(secretsmanager.get_secret_value(
            SecretId='GitHub/FarrOut/connection',
        )['SecretString'])
        connection_arn_ = connection_secret_value['FarrOut']

        CfnOutput(self, 'ConnectionArn',
                  description='ConnectionArn',
                  value=connection_arn_,
                  )

        if connection_secret.secret_value is None:
            logger.warning('Unable to retrieve GitHub Connection!')
        else:
            logger.info('Found GitHub Connection.')

        pipeline = CodePipeline(self, "Sandpipe",
                                pipeline_name="Sandpipe",
                                cross_account_keys=True,
                                synth=ShellStep("Synth",
                                                input=CodePipelineSource.connection(
                                                    "FarrOut/CloudVirtualMachine", "main",
                                                    connection_arn=connection_arn_,
                                                ),
                                                commands=["npm install -g aws-cdk",
                                                          "python -m pip install -r requirements.txt",
                                                          "cdk synth"]
                                                )
                                )
