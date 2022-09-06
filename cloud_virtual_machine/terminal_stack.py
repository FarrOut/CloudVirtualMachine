from aws_cdk import (

    Duration,
    Stack,
    aws_ec2 as ec2,
    aws_logs as logs, CfnOutput, RemovalPolicy,
)
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy
from aws_cdk.aws_s3 import Bucket
from constructs import Construct


class TerminalStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, whitelisted_peer: ec2.Peer, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        debug_mode = True  # TODO debugging

        # =====================
        # NETWORKING
        # =====================
        vpc = ec2.Vpc(self, "VPC",
                      max_azs=1,
                      )

        # =====================
        # SECURITY
        # =====================
        key_name = 'mykey'
        outer_perimeter_security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                                           vpc=vpc,
                                                           description="Allow ssh access to ec2 instances",
                                                           allow_all_outbound=True
                                                           )

        outer_perimeter_security_group.add_ingress_rule(whitelisted_peer, ec2.Port.tcp(22),
                                                        "allow ssh access from the world")
        outer_perimeter_security_group.add_ingress_rule(whitelisted_peer, ec2.Port.udp_range(60000, 61000),
                                                        "allow mosh access from the world")

        role = Role(self, "MyInstanceRole",
                    assumed_by=ServicePrincipal("ec2.amazonaws.com")
                    )
        # role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
        role.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AWSCloudFormationFullAccess"))
        role.apply_removal_policy(RemovalPolicy.DESTROY)

        workbucket = Bucket.from_bucket_name(self, "ImportedWorkbucket", bucket_name='gfarr-workbucket')
        workbucket.grant_read(role)

        # =====================
        # STORAGE
        # =====================

        # =====================
        # COMPUTING
        # =====================

        # CentOS
        # centos_bootstrapping = ec2.UserData.for_linux()
        # centos_bootstrapping.add_commands()
        # amalin_image = ec2.MachineImage.latest_amazon_linux(user_data=centos_bootstrapping)

        # Ubuntu
        ubuntu_bootstrapping = ec2.UserData.for_linux()

        # # https://aws.amazon.com/premiumsupport/knowledge-center/install-cloudformation-scripts/
        # # https://gist.github.com/mmasko/66d34b651642525c63cd39251e0c2a8b#gistcomment-3931793
        ubuntu_bootstrapping.add_commands(
            'sudo apt-get -y update',
            'sudo apt-get -y upgrade',
            'sudo apt-get -y install python3 python3-pip unzip',

            # Download Cloudformation Helper Scripts
            # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-helper-scripts-reference.html
            'wget https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-py3-latest.zip',
            'python3 -m easy_install --script-dir /opt/aws/bin aws-cfn-bootstrap-py3-latest.zip',
        )

        # Look up the most recent image matching a set of AMI filters.
        # In this case, look up the Ubuntu instance AMI
        # in the 'name' field:
        ubuntu_image = ec2.LookupMachineImage(
            # Canonical, Ubuntu, 20.04 LTS, amd64 focal image build on 2021-04-30
            # ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20210430
            name="ubuntu/images/*ubuntu-focal-20.04-*-20210430",
            owners=["099720109477"],
            filters={'architecture': ['x86_64']},
            user_data=ubuntu_bootstrapping,
        )

        image = ubuntu_image

        if debug_mode:
            CfnOutput(self, 'MachineImageOutput',
                      value=str(image.get_image(self).image_id),
                      description='MachineImageId',
                      )
            # CfnOutput(self, 'MachineImageUserDataOutput',
            #           value=str(image.get_image(self).user_data.render()),
            #           description='MachineImage UserData',
            #           )

        # View instance Logs in the Console
        # https: // docs.aws.amazon.com / systems - manager / latest / userguide / monitoring - cloudwatch - agent.html
        # https: // docs.aws.amazon.com / AmazonCloudWatch / latest / monitoring / Install - CloudWatch - Agent - New - Instances - CloudFormation.html
        # https://aws.amazon.com/blogs/devops/view-cloudformation-logs-in-the-console/
        # https://s3.amazonaws.com/cloudformation-templates-us-east-1/CloudWatch_Logs.template
        instance_log_group = logs.LogGroup.from_log_group_name(self, 'InstanceLogGroup',
                                                               log_group_name='InstanceLogGroup')

        working_dir = '/home/ubuntu/cfn-init/'
        # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-init.html
        init_ubuntu = ec2.CloudFormationInit.from_config_sets(
            config_sets={
                # Applies the configs below in this order
                "packaging": ['install_snap'],
                "logging": ['install_cw_agent'],
                "testing": [],
                "devops": ['docker'],
                "sysadmin": ['awscli', "aws-sam-cli", "cfn-cli"],
                'connectivity': ['install_mosh', 'install_vnc'],
            },
            configs={
                'docker': ec2.InitConfig([
                    ec2.InitPackage.apt(
                        package_name='ca-certificates',
                    ),
                    ec2.InitPackage.apt(
                        package_name='curl',
                    ),
                    ec2.InitPackage.apt(
                        package_name='gnupg',
                    ),
                    ec2.InitPackage.apt(
                        package_name='lsb-release',
                    ),
                    ec2.InitCommand.shell_command(
                        'sudo mkdir -p /etc/apt/keyrings',
                        cwd=working_dir,
                    ),
                    ec2.InitCommand.shell_command(
                        'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o '
                        '/etc/apt/keyrings/docker.gpg',
                        cwd=working_dir,
                    ),
                    ec2.InitCommand.shell_command(
                        'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] '
                        'https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee '
                        '/etc/apt/sources.list.d/docker.list > /dev/null',
                        cwd=working_dir,
                    ),
                    ec2.InitCommand.shell_command(
                        'apt update -y',
                        cwd=working_dir,
                    ),

                    ec2.InitPackage.apt(
                        package_name='docker-ce',
                    ),
                    ec2.InitPackage.apt(
                        package_name='docker-ce-cli',
                    ),
                    ec2.InitPackage.apt(
                        package_name='containerd.io',
                    ),
                    ec2.InitPackage.apt(
                        package_name='docker-compose-plugin',
                    ),
                ]),

                'awscli': ec2.InitConfig([
                    # https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
                    ec2.InitFile.from_url(
                        file_name=working_dir + 'awscliv2.zip',
                        url="https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip",
                    ),
                    ec2.InitPackage.apt(
                        package_name='unzip',
                    ),
                    ec2.InitCommand.shell_command(
                        'unzip awscliv2.zip',
                        cwd=working_dir,
                    ),
                    ec2.InitCommand.shell_command(
                        "sudo ./aws/install",
                        cwd=working_dir,
                    ),
                ]),
                'aws-sam-cli': ec2.InitConfig([
                    # Download installer package
                    # https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-linux.html#serverless-sam-cli-install-linux-sam-cli
                    ec2.InitFile.from_url(
                        file_name=working_dir + 'aws-sam-cli-linux-x86_64.zip',
                        url="https://github.com/aws/aws-sam-cli/releases/latest/download/aws-sam-cli-linux-x86_64.zip",
                    ),

                    # Install unzip
                    ec2.InitPackage.apt(
                        package_name='unzip',
                    ),

                    #  Extract
                    ec2.InitCommand.shell_command(
                        'unzip aws-sam-cli-linux-x86_64.zip -d sam-installation/',
                        cwd=working_dir,
                    ),

                    #  Install
                    ec2.InitCommand.shell_command(
                        "sudo ./sam-installation/install",
                        cwd=working_dir,
                    ),

                    #  Check version
                    ec2.InitCommand.shell_command(
                        "sam --version",
                        cwd=working_dir,
                    ),
                ]),
                'cfn-cli': ec2.InitConfig([
                    # Pin dependencies' versions to workaround conflicts
                    #
                    # https://stackoverflow.com/a/73199422
                    # https://github.com/aws-cloudformation/cloudformation-cli/issues/864
                    # https://github.com/aws-cloudformation/cloudformation-cli/issues/899
                    ec2.InitCommand.shell_command(
                        "pip install --upgrade requests urllib3",
                        cwd=working_dir,
                    ),
                    ec2.InitCommand.shell_command(
                        "pip install markupsafe==2.0.1 pyyaml==5.4.1",
                        cwd=working_dir,
                    ),
                    ec2.InitCommand.shell_command(
                        "pip install werkzeug==2.1.2 --no-deps",
                        cwd=working_dir,
                    ),

                    #  Install
                    # https://docs.aws.amazon.com/cloudformation-cli/latest/userguide/what-is-cloudformation-cli.html#resource-type-setup
                    ec2.InitCommand.shell_command(
                        "pip install cloudformation-cli cloudformation-cli-java-plugin cloudformation-cli-go-plugin "
                        "cloudformation-cli-python-plugin cloudformation-cli-typescript-plugin",
                        cwd=working_dir,
                    ),
                ]),
                'install_snap': ec2.InitConfig([
                    ec2.InitPackage.apt(
                        package_name='snap',
                    ),
                ]),
                'install_vnc': ec2.InitConfig([
                    # https://en.wikipedia.org/wiki/X11vnc
                    # https://askubuntu.com/questions/229989/how-to-setup-x11vnc-to-access-with-graphical-login-screen/

                    ec2.InitPackage.apt(
                        package_name='x11vnc',
                    ),

                    # ec2.InitPackage.apt(
                    #     package_name='xfce4',
                    # ),
                    # ec2.InitPackage.apt(
                    #     package_name='xfce4-goodies',
                    # ),
                    # ec2.InitPackage.apt(
                    #     package_name='xorg',
                    # ),
                    # ec2.InitPackage.apt(
                    #     package_name='dbus-x11',
                    # ),
                    # ec2.InitPackage.apt(
                    #     package_name='x11-xserver-utils',
                    # ),
                ]),
                'install_mosh': ec2.InitConfig([
                    ec2.InitPackage.apt(
                        package_name='mosh',
                    ),
                ]),
                'install_cw_agent': ec2.InitConfig([

                    # Manually create or edit the CloudWatch agent configuration file
                    # https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html

                    # Installing and running the CloudWatch agent on your servers
                    # https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent-commandline-fleet.html

                    ec2.InitFile.from_url(
                        file_name=working_dir + '/amazon-cloudwatch-agent.deb',
                        url='https://s3.amazonaws.com/amazoncloudwatch-agent/debian/amd64/latest/amazon-cloudwatch'
                            '-agent.deb'),
                    ec2.InitCommand.shell_command(
                        shell_command='dpkg -i -E ./amazon-cloudwatch-agent.deb',
                        cwd=working_dir)

                    # TODO Design config file and start CloudWatch agent service
                    # Installing the CloudWatch agent on new instances using AWS CloudFormation
                    # https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent-New-Instances-CloudFormation.html
                ])
            }
        )

        init = init_ubuntu
        instance = ec2.Instance(self, "Instance",
                                user_data_causes_replacement=True,
                                vpc=vpc,
                                instance_type=ec2.InstanceType.of(
                                    ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.LARGE),
                                machine_image=image,
                                key_name=key_name,
                                security_group=outer_perimeter_security_group,
                                role=role,
                                init=init,

                                # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/ApplyCloudFormationInitOptions.html
                                init_options=ec2.ApplyCloudFormationInitOptions(
                                    # Optional, which configsets to activate (['default'] by default)
                                    config_sets=["packaging", "connectivity", 'sysadmin', 'devops'],

                                    # Don’t fail the instance creation when cfn-init fails. You can use this to
                                    # prevent CloudFormation from rolling back when instances fail to start up,
                                    # to help in debugging. Default: false
                                    ignore_failures=debug_mode,

                                    # Optional, how long the installation is expected to take (5 minutes by default)
                                    timeout=Duration.minutes(10),

                                    # Optional, whether to include the --url argument when running cfn-init and cfn-signal commands (false by default)
                                    include_url=False,

                                    # Optional, whether to include the --role argument when running cfn-init and cfn-signal commands (false by default)
                                    include_role=False
                                ),
                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                )

        # TODO convert to Spot instances
        #
        # Launching EC2 Spot Instances via EC2 Auto Scaling group
        # https://ec2spotworkshops.com/launching_ec2_spot_instances/asg.html

        # asg = autoscaling.AutoScalingGroup(self, "ASG",
        #                                    vpc=vpc,
        #                                    instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3,
        #                                                                      ec2.InstanceSize.LARGE),
        #                                    machine_image=image,
        #                                    security_group=outer_perimeter_security_group,
        #                                    associate_public_ip_address=True,
        #                                    allow_all_outbound=True,
        #                                    role=role,
        #                                    key_name=key_name,
        #                                    init=init,
        #                                    # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/ApplyCloudFormationInitOptions.html
        #                                    init_options=autoscaling.ApplyCloudFormationInitOptions(
        #                                        # Optional, which configsets to activate (['default'] by default)
        #                                        config_sets=["connectivity"],
        #
        #                                        # Don’t fail the instance creation when cfn-init fails. You can use this to
        #                                        # prevent CloudFormation from rolling back when instances fail to start up,
        #                                        # to help in debugging. Default: false
        #                                        ignore_failures=debug_mode,
        #
        #                                        # Optional, whether to include the --url argument when running cfn-init and cfn-signal commands (false by default)
        #                                        include_url=False,
        #
        #                                        # Optional, whether to include the --role argument when running cfn-init and cfn-signal commands (false by default)
        #                                        include_role=False
        #                                    ),
        #                                    signals=autoscaling.Signals.wait_for_all(
        #                                        timeout=cdk.Duration.minutes(2)
        #                                    ),
        #                                    update_policy=autoscaling.UpdatePolicy.replacing_update(),
        #                                    # Be aware this will reset the size of your AutoScalingGroup on every deployment.
        #                                    # See https://github.com/aws/aws-cdk/issues/5215
        #                                    desired_capacity=1,
        #                                    min_capacity=0,
        #                                    max_capacity=5,
        #                                    vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        #                                    )

        # TODO Scale out or in based on time.
        # https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_autoscaling/AutoScalingGroup.html#aws_cdk.aws_autoscaling.AutoScalingGroup.scale_on_schedule
        # To have a warm pool ready for the day ahead

        CfnOutput(self, 'InstancePublicDNSname',
                  value=instance.instance_public_dns_name,
                  description='Publicly-routable DNS name for this instance.',
                  )

        user = 'ubuntu'
        ssh_command = 'ssh' + ' -i ' + key_name + '.pem ' + user + '@' + instance.instance_public_dns_name
        CfnOutput(self, 'InstanceSSHcommand',
                  value=ssh_command,
                  description='Command to SSH into instance.',
                  )
