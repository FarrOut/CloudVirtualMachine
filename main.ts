import { Construct } from "constructs";
import { App, TerraformStack } from "cdktf";
import { NetworkStack } from "./stacks/network-stack";
import { AwsProvider } from "@cdktf/provider-aws/lib/provider";
import { Stack } from "aws-cdk-lib";

export interface NestedStackConfig {
  environment: string;
  region?: string;
}

class AwsCloudformationStack extends Stack{
  constructor(scope: Construct, id: string) {
    super(scope, id);

    new NetworkStack(this, "network", {  });

// new TerminalStack(this, "terminal", config);

  }
}

class CloudTerminalStack extends TerraformStack {
  constructor(scope: Construct, id: string, config: NestedStackConfig) {
    super(scope, id);

    new AwsProvider(this, "AWS", config);
  
    new AwsCloudformationStack(this, "CloudTerminalStack");

  }
}

const app = new App();
new CloudTerminalStack(app, "CloudTerminal", { environment: 'dev', region: 'af-south-1' });
app.synth();
