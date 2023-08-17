import { Construct } from "constructs";
// import { TerraformOutput } from "cdktf";
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { NestedStack } from "aws-cdk-lib";

interface VpcConfig {
  cidrBlock?: string
}

export class NetworkStack extends NestedStack {
  constructor(scope: Construct, id: string, _config: VpcConfig) {
    super(scope, id);

    new ec2.Vpc(this, 'VPC');

    // new TerraformOutput(this, "VpcId", {
    //   value: vpc.vpcId,
    //   description: "VPC ID",          
    // });



  }
}
