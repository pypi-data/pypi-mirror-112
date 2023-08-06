# Welcome to cdk-vscode-fargate

`cdk-vscode-fargate` is a JSII construct library for AWS CDK that allows you to deploy [Code-server](https://github.com/orgs/linuxserver/packages/container/package/code-server) running VS Code remotely, on a AWS Fargate container.

By deploying the `VSCodeFargate` construct, the following resources will be created:

1. VPC (if not passed in as a prop)
2. ACM DNS validated certificate
3. ECS Cluster
4. EFS file system
5. ALB Fargate Service
6. Security Groups
7. Secrets Manager secret (for login authorization)

![diagram](./diagram.png)

## Howto

Create a new project with AWS CDK

```sh
$ mkdir my-vscode-fargate && cd my-vscode-fargate
# initialize the AWS CDK project
$ cdk init -l typescript
# install the cdk-vscode-fargate npm module
$ yarn add cdk-vscode-fargate
```

# AWS CDK sample

Building your serverless VS Code service with the `VSCodeFargate` construct:

Update `./lib/my-vscode-fargate-stack.ts`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ec2 as ec2
import aws_cdk.core as cdk
from cdk_vscode_fargate import VSCodeFargate

class CdkStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        subdomain = process.env.VSCODE_SUBDOMAIN ?? "vscode"
        domain_name = process.env.VSCODE_DOMAIN_NAME ?? "mydomain.com"

        vpc = ec2.Vpc.from_lookup(self, "Vpc",
            is_default=True
        )

        VSCodeFargate(self, "MyVSCodeFargate",
            domain_name=domain_name,
            subdomain=subdomain,
            vpc=vpc
        )
```

diff the CDK stack:

```sh
$ cdk deploy
```

deploy the CDK stack:

```sh
$ cdk diff
```

On deploy completion, the subdomain/domain name assigned to the load balancer will be returned in the Output. Click the URL and you will see the login page:

![vscode-fargate-login](./images/vscode-fargate-login.png)
