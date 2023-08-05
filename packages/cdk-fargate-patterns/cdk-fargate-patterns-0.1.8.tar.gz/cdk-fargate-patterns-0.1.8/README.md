[![NPM version](https://badge.fury.io/js/cdk-fargate-patterns.svg)](https://badge.fury.io/js/cdk-fargate-patterns)
[![PyPI version](https://badge.fury.io/py/cdk-fargate-patterns.svg)](https://badge.fury.io/py/cdk-fargate-patterns)
[![Release](https://github.com/pahud/cdk-fargate-patterns/actions/workflows/release.yml/badge.svg)](https://github.com/pahud/cdk-fargate-patterns/actions/workflows/release.yml)

# cdk-fargate-patterns

CDK patterns for serverless container with AWS Fargate

# `DualAlbFargateService`

Inspired by *Vijay Menon* from the [AWS blog post](https://aws.amazon.com/blogs/containers/how-to-use-multiple-load-balancer-target-group-support-for-amazon-ecs-to-access-internal-and-external-service-endpoint-using-the-same-dns-name/) introduced in 2019, `DualAlbFargateService` allows you to create one or many fargate services with both internet-facing ALB and internal ALB associated with all services. With this pattern, fargate services will be allowed to intercommunicat via internal ALB while external inbound traffic will be spread across the same service tasks through internet-facing ALB.

The sample below will create 3 fargate services associated with both external and internal ALBs. The internal ALB will have an alias(`internal.svc.local`) auto-configured from Route 53 so services can communite through the private ALB endpoint.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DualAlbFargateService(stack, "Service",
    spot=True, # FARGATE_SPOT only cluster
    tasks=[{
        "listener_port": 80,
        "task": order_task,
        "desired_count": 2,
        # customize the service autoscaling policy
        "scaling_policy": {
            "max_capacity": 20,
            "request_per_target": 1000,
            "target_cpu_utilization": 50
        }
    }, {"listener_port": 8080, "task": customer_task, "desired_count": 2}, {"listener_port": 9090, "task": product_task, "desired_count": 2}
    ],
    route53_ops={
        "zone_name": zone_name, # svc.local
        "external_alb_record_name": external_alb_record_name, # external.svc.local
        "internal_alb_record_name": internal_alb_record_name
    }
)
```

## Fargate Spot Support

By enabling the `spot` property, 100% fargate spot tasks will be provisioned to help you save up to 70%. Check more details about [Fargate Spot](https://aws.amazon.com/about-aws/whats-new/2019/12/aws-launches-fargate-spot-save-up-to-70-for-fault-tolerant-applications/?nc1=h_ls). This is a handy catch-all flag to force all tasks to be `FARGATE_SPOT` only.

To specify mixed strategy with partial `FARGATE` and partial `FARGATE_SPOT`, specify the `capacityProviderStrategy` for individual tasks like

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DualAlbFargateService(stack, "Service",
    tasks=[{
        "listener_port": 8080,
        "task": customer_task,
        "desired_count": 2,
        "capacity_provider_strategy": [{
            "capacity_provider": "FARGATE",
            "base": 1,
            "weight": 1
        }, {
            "capacity_provider": "FARGATE_SPOT",
            "base": 0,
            "weight": 3
        }
        ]
    }
    ]
)
```

The custom capacity provider strategy will be applied if `capacityProviderStretegy` is specified, otherwise, 100% spot will be used when `spot: true`. The default policy is 100% Fargate on-demand.

## ECS Exec

Simply turn on the `enableExecuteCommand` property to enable the [ECS Exec](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html) support for all services.

## Internal or External Only

By default, all task(s) defined in the `DualAlbFargateService` will be registered to both external and internal ALBs.
Set `accessibility` to make it internal only, external only, or both.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DualAlbFargateService(stack, "Service",
    tasks=[{"listener_port": 8080, "task": task1, "accessibility": LoadBalancerAccessibility.INTERNAL_ONLY}, {"listener_port": 8081, "task": task2, "accessibility": LoadBalancerAccessibility.EXTERNAL_ONLY}, {"listener_port": 8082, "task": task3}
    ]
)
```

Please note if all tasks are defined as `INTERNAL_ONLY`, no external ALB will be created. Similarly, no internal ALB
will be created if all defined as `EXTERNAL_ONLY`.

## VPC Subnets

By default, all tasks will be deployed in the private subnets. You will need the NAT gateway for the default route associated with the private subnets to ensure the task can successfully pull the container images.

However, you are allowed to specify `vpcSubnets` to customize the subnet selection.

To deploy all tasks in public subnets, one per AZ:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DualAlbFargateService(stack, "Service",
    vpc_subnets={
        "subnet_type": ec2.SubnetType.PUBLIC,
        "one_per_az": True
    }, ...
)
```

This will implicitly enable the `auto assign public IP` for each fargate task so the task can successfully pull the container images from external registry. However, the ingress traffic will still be balanced via the external ALB.

To deploy all tasks in specific subnets:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DualAlbFargateService(stack, "Service",
    vpc_subnets={
        "subnets": [
            ec2.Subnet.from_subnet_id(stack, "sub-1a", "subnet-0e9460dbcfc4cf6ee"),
            ec2.Subnet.from_subnet_id(stack, "sub-1b", "subnet-0562f666bdf5c29af"),
            ec2.Subnet.from_subnet_id(stack, "sub-1c", "subnet-00ab15c0022872f06")
        ]
    }, ...
)
```

## Sample Application

This repository comes with a sample applicaiton with 3 services in Golang. On deployment, the `Order` service will be exposed externally on external ALB port `80` and all requests to the `Order` service will trigger sub-requests internally to another other two services(`product` and `customer`) through the internal ALB and eventually aggregate the response back to the client.

![](images/DualAlbFargateService.svg)

## Deploy

To deploy the sample application in you default VPC:

```sh
// install first
$ yarn install
// compile the ts to js
$ yarn build
$ npx cdk --app lib/integ.default.js -c use_default_vpc=1 diff
$ npx cdk --app lib/integ.default.js -c use_default_vpc=1 deploy
```

On deployment complete, you will see the external ALB endpoint in the CDK output. `cURL` the external HTTP endpoint and you should be able to see the aggregated response.

```sh
$ curl http://demo-Servi-EH1OINYDWDU9-1397122594.ap-northeast-1.elb.amazonaws.com

{"service":"order", "version":"1.0"}
{"service":"product","version":"1.0"}
{"service":"customer","version":"1.0"}
```

# `WordPress`

Use the `WordPress` construct to create a serverless **WordPress** service with AWS Fargate, Amazon EFS filesystem and Aurora serverless database. All credentials auto generated from the **AWS Secret Manager** and securely inject the credentials into the serverless container with the auto generated IAM task execution role.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
WordPress(stack, "WP",
    aurora_serverless=True,
    spot=True,
    enable_execute_command=True
)
```
