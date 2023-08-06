'''
# CloudWatch Alarm to Chat Platforms CDK Construct

This construct creates an SNS topic and Lambda used to translate CloudWatch alarms into notifications set to various chat platforms. Currently only Microsoft Teams is supported.

Example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
import aws_cdk.aws_s3 as s3
from aws_cdk.aws_lambda import Runtime
import aws_cdk.aws_lambda_python as _lambda
import aws_cdk.aws_cloudwatch as cloudwatch
import aws_cdk.aws_cloudwatch_actions as cw_actions
import ......Cloudwatch_Alarms_to_Chat_Platforms.src.index as notifications
import path as path
import aws_cdk.aws_events as events
import aws_cdk.aws_events_targets as targets
from aws_cdk.assert import count_resources

class TestCdkConstructStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        failure_lambda = _lambda.PythonFunction(self, "FailureLambda",
            entry=path.join(__dirname, "..", "functions", "failureLambda"),
            runtime=Runtime.PYTHON_3_8
        )

        rule = events.Rule(self, "Schedule",
            schedule=events.Schedule.rate(cdk.Duration.minutes(1))
        )

        rule.add_target(targets.LambdaFunction(failure_lambda))

        errors = failure_lambda.metric_errors()

        errors.with(
            period=cdk.Duration.minutes(1)
        )

        alarm = errors.create_alarm(self, "Alarm",
            alarm_name="Example Lambda Alarm",
            alarm_description="This alarm will trigger when the lambda fails 2 out of 3 times in a given period",
            threshold=2,
            evaluation_periods=3,
            period=cdk.Duration.minutes(1)
        )

        note = notifications.CloudwatchAlarmsToTeamsConstruct(self, "Notification",
            webhook_url="https://test.webhook.office.com/webhookb2/example-webhook-goes-here"
        )

        note.add_alarm_to_teams_notification(alarm)
```

## API

For specific API usage see the [API Docs](https://github.com/1davidmichael/Cloudwatch-Alarms-to-Chat-Platforms/blob/main/API.md)
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

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.core


class CloudwatchAlarmsToTeamsConstruct(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cloudwatch-alarms-to-teams.CloudwatchAlarmsToTeamsConstruct",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        webhook_url: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param webhook_url: Provide a webhook url.
        '''
        props = CloudwatchAlarmsToTeamsConstructProps(webhook_url=webhook_url)

        jsii.create(CloudwatchAlarmsToTeamsConstruct, self, [scope, id, props])

    @jsii.member(jsii_name="addAlarmToTeamsNotification")
    def add_alarm_to_teams_notification(
        self,
        alarm: aws_cdk.aws_cloudwatch.Alarm,
    ) -> None:
        '''
        :param alarm: -
        '''
        return typing.cast(None, jsii.invoke(self, "addAlarmToTeamsNotification", [alarm]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.SingletonFunction:
        return typing.cast(aws_cdk.aws_lambda.SingletonFunction, jsii.get(self, "lambdaFunction"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="topic")
    def topic(self) -> aws_cdk.aws_sns.Topic:
        return typing.cast(aws_cdk.aws_sns.Topic, jsii.get(self, "topic"))


@jsii.data_type(
    jsii_type="cloudwatch-alarms-to-teams.CloudwatchAlarmsToTeamsConstructProps",
    jsii_struct_bases=[],
    name_mapping={"webhook_url": "webhookUrl"},
)
class CloudwatchAlarmsToTeamsConstructProps:
    def __init__(self, *, webhook_url: builtins.str) -> None:
        '''
        :param webhook_url: Provide a webhook url.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "webhook_url": webhook_url,
        }

    @builtins.property
    def webhook_url(self) -> builtins.str:
        '''Provide a webhook url.'''
        result = self._values.get("webhook_url")
        assert result is not None, "Required property 'webhook_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchAlarmsToTeamsConstructProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudwatchAlarmsToTeamsConstruct",
    "CloudwatchAlarmsToTeamsConstructProps",
]

publication.publish()
