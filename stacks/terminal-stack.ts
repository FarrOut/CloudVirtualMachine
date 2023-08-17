import { Construct } from "constructs";
import { TerraformOutput, TerraformStack, Token } from "cdktf";
import { AwsProvider } from "@cdktf/provider-aws/lib/provider";
import { DataAwsAmi } from "@cdktf/provider-aws/lib/data-aws-ami";
import { Instance } from "@cdktf/provider-aws/lib/instance";

interface MyMultiStackConfig {
  environment: string;
  region?: string;
}

export class TerminalStack extends TerraformStack {
  constructor(scope: Construct, id: string, config: MyMultiStackConfig) {
    super(scope, id);


    // define resources here
    new AwsProvider(this, "AWS", config);

    const ubuntu = new DataAwsAmi(this, "ubuntu", {
      filter: [
        {
          name: "name",
          values: ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"],
        },
        {
          name: "virtualization-type",
          values: ["hvm"],
        },
      ],
      mostRecent: true,
      owners: ["099720109477"],
    });

    const instance = new Instance(this, "web", {
      ami: Token.asString(ubuntu.id),
      instanceType: "t3.micro",
      tags: {
        Name: "HelloWorld",
      },
    });

    new TerraformOutput(this, "InstanceArn", {
      value: instance.arn,
    });



  }
}
