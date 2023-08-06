'''
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
        "task": order_task,
        "desired_count": 2,
        "internal": {"port": 443, "cert": cert},
        "external": {"port": 80},
        # customize the service autoscaling policy
        "scaling_policy": {
            "max_capacity": 20,
            "request_per_target": 1000,
            "target_cpu_utilization": 50
        }
    }, {"task": customer_task, "desired_count": 2, "internal": {"port": 8080}}, {"task": product_task, "desired_count": 2, "internal": {"port": 9090}}
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
        "task": customer_task,
        "internal": {"port": 8080},
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

## Internal, External or Both

Specify the `internal` or `external` property to expose your service internally, externally or both.

The `cert` property implies `HTTPS` protocol.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
DualAlbFargateService(stack, "Service",
    tasks=[{"task": task1, "internal": {"port": 8080}}, {"task": task2, "external": {"port": 8081}}, {
        "task": task3,
        "external": {"port": 443, "cert": my_acm_cert},
        "internal": {"port": 8888}
    }
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

To deploy with HTTPS-only with existing ACM certificate in your default VPC:

```sh
$ npx cdk --app lib/integ.default.js deploy -c use_default_vpc=1 -c ACM_CERT_ARN=<YOUR_ACM_CERT_ARN>
```

On deployment complete, you will see the external ALB endpoint in the CDK output. `cURL` the external HTTP endpoint and you should be able to see the aggregated response.

```sh
$ curl http://demo-Servi-EH1OINYDWDU9-1397122594.ap-northeast-1.elb.amazonaws.com
or
$ curl https://<YOUR_CUSTOM_DOMAIN_NAME>

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
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.core


class DualAlbFargateService(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-fargate-patterns.DualAlbFargateService",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        tasks: typing.Sequence["FargateTaskProps"],
        enable_execute_command: typing.Optional[builtins.bool] = None,
        route53_ops: typing.Optional["Route53Options"] = None,
        spot: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param tasks: 
        :param enable_execute_command: Whether to enable ECS Exec support. Default: false
        :param route53_ops: 
        :param spot: create a FARGATE_SPOT only cluster. Default: false
        :param vpc: 
        :param vpc_subnets: The subnets to associate with the service. Default: - { subnetType: ec2.SubnetType.PRIVATE, }
        '''
        props = DualAlbFargateServiceProps(
            tasks=tasks,
            enable_execute_command=enable_execute_command,
            route53_ops=route53_ops,
            spot=spot,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(DualAlbFargateService, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="service")
    def service(self) -> typing.List[aws_cdk.aws_ecs.FargateService]:
        '''The service(s) created from the task(s).'''
        return typing.cast(typing.List[aws_cdk.aws_ecs.FargateService], jsii.get(self, "service"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''The VPC.'''
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="externalAlb")
    def external_alb(
        self,
    ) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer]:
        '''The external ALB.'''
        return typing.cast(typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer], jsii.get(self, "externalAlb"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="internalAlb")
    def internal_alb(
        self,
    ) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer]:
        '''The internal ALB.'''
        return typing.cast(typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer], jsii.get(self, "internalAlb"))


@jsii.data_type(
    jsii_type="cdk-fargate-patterns.DualAlbFargateServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "tasks": "tasks",
        "enable_execute_command": "enableExecuteCommand",
        "route53_ops": "route53Ops",
        "spot": "spot",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class DualAlbFargateServiceProps:
    def __init__(
        self,
        *,
        tasks: typing.Sequence["FargateTaskProps"],
        enable_execute_command: typing.Optional[builtins.bool] = None,
        route53_ops: typing.Optional["Route53Options"] = None,
        spot: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        '''
        :param tasks: 
        :param enable_execute_command: Whether to enable ECS Exec support. Default: false
        :param route53_ops: 
        :param spot: create a FARGATE_SPOT only cluster. Default: false
        :param vpc: 
        :param vpc_subnets: The subnets to associate with the service. Default: - { subnetType: ec2.SubnetType.PRIVATE, }
        '''
        if isinstance(route53_ops, dict):
            route53_ops = Route53Options(**route53_ops)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "tasks": tasks,
        }
        if enable_execute_command is not None:
            self._values["enable_execute_command"] = enable_execute_command
        if route53_ops is not None:
            self._values["route53_ops"] = route53_ops
        if spot is not None:
            self._values["spot"] = spot
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def tasks(self) -> typing.List["FargateTaskProps"]:
        result = self._values.get("tasks")
        assert result is not None, "Required property 'tasks' is missing"
        return typing.cast(typing.List["FargateTaskProps"], result)

    @builtins.property
    def enable_execute_command(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable ECS Exec support.

        :default: false

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html
        '''
        result = self._values.get("enable_execute_command")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def route53_ops(self) -> typing.Optional["Route53Options"]:
        result = self._values.get("route53_ops")
        return typing.cast(typing.Optional["Route53Options"], result)

    @builtins.property
    def spot(self) -> typing.Optional[builtins.bool]:
        '''create a FARGATE_SPOT only cluster.

        :default: false
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''The subnets to associate with the service.

        :default:

        -

        {
        subnetType: ec2.SubnetType.PRIVATE,
        }
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DualAlbFargateServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-fargate-patterns.FargateTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "task": "task",
        "capacity_provider_strategy": "capacityProviderStrategy",
        "desired_count": "desiredCount",
        "external": "external",
        "health_check": "healthCheck",
        "internal": "internal",
        "scaling_policy": "scalingPolicy",
    },
)
class FargateTaskProps:
    def __init__(
        self,
        *,
        task: aws_cdk.aws_ecs.FargateTaskDefinition,
        capacity_provider_strategy: typing.Optional[typing.Sequence[aws_cdk.aws_ecs.CapacityProviderStrategy]] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        external: typing.Optional["LoadBalancerAccessibility"] = None,
        health_check: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.HealthCheck] = None,
        internal: typing.Optional["LoadBalancerAccessibility"] = None,
        scaling_policy: typing.Optional["ServiceScalingPolicy"] = None,
    ) -> None:
        '''Task properties for the Fargate.

        :param task: 
        :param capacity_provider_strategy: Customized capacity provider strategy.
        :param desired_count: desired number of tasks for the service. Default: 1
        :param external: The external ALB listener. Default: - no external listener
        :param health_check: health check from elbv2 target group.
        :param internal: The internal ALB listener. Default: - no internal listener
        :param scaling_policy: service autoscaling policy. Default: - { maxCapacity: 10, targetCpuUtilization: 50, requestsPerTarget: 1000 }
        '''
        if isinstance(external, dict):
            external = LoadBalancerAccessibility(**external)
        if isinstance(health_check, dict):
            health_check = aws_cdk.aws_elasticloadbalancingv2.HealthCheck(**health_check)
        if isinstance(internal, dict):
            internal = LoadBalancerAccessibility(**internal)
        if isinstance(scaling_policy, dict):
            scaling_policy = ServiceScalingPolicy(**scaling_policy)
        self._values: typing.Dict[str, typing.Any] = {
            "task": task,
        }
        if capacity_provider_strategy is not None:
            self._values["capacity_provider_strategy"] = capacity_provider_strategy
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if external is not None:
            self._values["external"] = external
        if health_check is not None:
            self._values["health_check"] = health_check
        if internal is not None:
            self._values["internal"] = internal
        if scaling_policy is not None:
            self._values["scaling_policy"] = scaling_policy

    @builtins.property
    def task(self) -> aws_cdk.aws_ecs.FargateTaskDefinition:
        result = self._values.get("task")
        assert result is not None, "Required property 'task' is missing"
        return typing.cast(aws_cdk.aws_ecs.FargateTaskDefinition, result)

    @builtins.property
    def capacity_provider_strategy(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ecs.CapacityProviderStrategy]]:
        '''Customized capacity provider strategy.'''
        result = self._values.get("capacity_provider_strategy")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ecs.CapacityProviderStrategy]], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''desired number of tasks for the service.

        :default: 1
        '''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def external(self) -> typing.Optional["LoadBalancerAccessibility"]:
        '''The external ALB listener.

        :default: - no external listener
        '''
        result = self._values.get("external")
        return typing.cast(typing.Optional["LoadBalancerAccessibility"], result)

    @builtins.property
    def health_check(
        self,
    ) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.HealthCheck]:
        '''health check from elbv2 target group.'''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[aws_cdk.aws_elasticloadbalancingv2.HealthCheck], result)

    @builtins.property
    def internal(self) -> typing.Optional["LoadBalancerAccessibility"]:
        '''The internal ALB listener.

        :default: - no internal listener
        '''
        result = self._values.get("internal")
        return typing.cast(typing.Optional["LoadBalancerAccessibility"], result)

    @builtins.property
    def scaling_policy(self) -> typing.Optional["ServiceScalingPolicy"]:
        '''service autoscaling policy.

        :default: - { maxCapacity: 10, targetCpuUtilization: 50, requestsPerTarget: 1000 }
        '''
        result = self._values.get("scaling_policy")
        return typing.cast(typing.Optional["ServiceScalingPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-fargate-patterns.LoadBalancerAccessibility",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "certificate": "certificate"},
)
class LoadBalancerAccessibility:
    def __init__(
        self,
        *,
        port: jsii.Number,
        certificate: typing.Optional[typing.Sequence[aws_cdk.aws_certificatemanager.ICertificate]] = None,
    ) -> None:
        '''The load balancer accessibility.

        :param port: The port of the listener.
        :param certificate: The ACM certificate for the HTTPS listener. Default: - no certificate(HTTP only)
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "port": port,
        }
        if certificate is not None:
            self._values["certificate"] = certificate

    @builtins.property
    def port(self) -> jsii.Number:
        '''The port of the listener.'''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_certificatemanager.ICertificate]]:
        '''The ACM certificate for the HTTPS listener.

        :default: - no certificate(HTTP only)
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_certificatemanager.ICertificate]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerAccessibility(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-fargate-patterns.Route53Options",
    jsii_struct_bases=[],
    name_mapping={
        "enable_load_balancer_alias": "enableLoadBalancerAlias",
        "external_alb_record_name": "externalAlbRecordName",
        "internal_alb_record_name": "internalAlbRecordName",
        "zone_name": "zoneName",
    },
)
class Route53Options:
    def __init__(
        self,
        *,
        enable_load_balancer_alias: typing.Optional[builtins.bool] = None,
        external_alb_record_name: typing.Optional[builtins.str] = None,
        internal_alb_record_name: typing.Optional[builtins.str] = None,
        zone_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enable_load_balancer_alias: Whether to configure the ALIAS for the LB. Default: true
        :param external_alb_record_name: the external ALB record name. Default: external
        :param internal_alb_record_name: the internal ALB record name. Default: internal
        :param zone_name: private zone name. Default: svc.local
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if enable_load_balancer_alias is not None:
            self._values["enable_load_balancer_alias"] = enable_load_balancer_alias
        if external_alb_record_name is not None:
            self._values["external_alb_record_name"] = external_alb_record_name
        if internal_alb_record_name is not None:
            self._values["internal_alb_record_name"] = internal_alb_record_name
        if zone_name is not None:
            self._values["zone_name"] = zone_name

    @builtins.property
    def enable_load_balancer_alias(self) -> typing.Optional[builtins.bool]:
        '''Whether to configure the ALIAS for the LB.

        :default: true
        '''
        result = self._values.get("enable_load_balancer_alias")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def external_alb_record_name(self) -> typing.Optional[builtins.str]:
        '''the external ALB record name.

        :default: external
        '''
        result = self._values.get("external_alb_record_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internal_alb_record_name(self) -> typing.Optional[builtins.str]:
        '''the internal ALB record name.

        :default: internal
        '''
        result = self._values.get("internal_alb_record_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_name(self) -> typing.Optional[builtins.str]:
        '''private zone name.

        :default: svc.local
        '''
        result = self._values.get("zone_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Route53Options(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-fargate-patterns.ServiceScalingPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "max_capacity": "maxCapacity",
        "request_per_target": "requestPerTarget",
        "target_cpu_utilization": "targetCpuUtilization",
    },
)
class ServiceScalingPolicy:
    def __init__(
        self,
        *,
        max_capacity: typing.Optional[jsii.Number] = None,
        request_per_target: typing.Optional[jsii.Number] = None,
        target_cpu_utilization: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_capacity: max capacity for the service autoscaling. Default: 10
        :param request_per_target: request per target. Default: 1000
        :param target_cpu_utilization: target cpu utilization. Default: 50
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if request_per_target is not None:
            self._values["request_per_target"] = request_per_target
        if target_cpu_utilization is not None:
            self._values["target_cpu_utilization"] = target_cpu_utilization

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''max capacity for the service autoscaling.

        :default: 10
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def request_per_target(self) -> typing.Optional[jsii.Number]:
        '''request per target.

        :default: 1000
        '''
        result = self._values.get("request_per_target")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_cpu_utilization(self) -> typing.Optional[jsii.Number]:
        '''target cpu utilization.

        :default: 50
        '''
        result = self._values.get("target_cpu_utilization")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceScalingPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DualAlbFargateService",
    "DualAlbFargateServiceProps",
    "FargateTaskProps",
    "LoadBalancerAccessibility",
    "Route53Options",
    "ServiceScalingPolicy",
]

publication.publish()
