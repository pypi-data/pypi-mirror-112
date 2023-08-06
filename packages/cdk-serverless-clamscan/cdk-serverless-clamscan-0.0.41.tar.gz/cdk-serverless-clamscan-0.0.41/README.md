# cdk-serverless-clamscan

[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cdk-serverless-clamscan/)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/cdk-serverless-clamscan)

An [aws-cdk](https://github.com/aws/aws-cdk) construct that uses [ClamAV®](https://www.clamav.net/) to scan objects in Amazon S3 for viruses. The construct provides a flexible interface for a system to act based on the results of a ClamAV virus scan.

![Overview](serverless-clamscan.png)

## Pre-Requisites

**Docker:** The ClamAV Lambda functions utilizes a [container image](https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/) that is built locally using [docker bundling](https://aws.amazon.com/blogs/devops/building-apps-with-aws-cdk/)

## Examples

This project uses [projen](https://github.com/projen/projen) and thus all the constructs follow language specific standards and naming patterns. For more information on how to translate the following examples into your desired language read the CDK guide on [Translating TypeScript AWS CDK code to other languages](https://docs.aws.amazon.com/cdk/latest/guide/multiple_languages.html)

### Example 1. (Default destinations with rule target)

<details><summary>typescript</summary>
<p>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_events import RuleTargetInput
from aws_cdk.aws_events_targets import SnsTopic
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_sns import Topic
from aws_cdk.core import Construct, Stack, StackProps
from cdk_serverless_clamscan import ServerlessClamscan

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        bucket_1 = Bucket(self, "rBucket1")
        bucket_2 = Bucket(self, "rBucket2")
        bucket_list = [bucket_1, bucket_2]
        sc = ServerlessClamscan(self, "rClamscan",
            buckets=bucket_list
        )
        bucket_3 = Bucket(self, "rBucket3")
        sc.add_source_bucket(bucket_3)
        infected_topic = Topic(self, "rInfectedTopic")
        sc.infected_rule.add_target(SnsTopic(infected_topic,
            message=RuleTargetInput.from_event_path("$.detail.responsePayload.message")
        ))
```

</p>
</details><details><summary>python</summary>
<p>

```python
from aws_cdk import (
  core as core,
  aws_events as events,
  aws_events_targets as events_targets,
  aws_s3 as s3,
  aws_sns as sns
)
from cdk_serverless_clamscan import ServerlessClamscan

class CdkTestStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    bucket_1 = s3.Bucket(self, "rBucket1")
    bucket_2 = s3.Bucket(self, "rBucket2")
    bucketList = [ bucket_1, bucket_2 ]
    sc = ServerlessClamscan(self, "rClamScan",
      buckets=bucketList,
    )
    bucket_3 = s3.Bucket(self, "rBucket3")
    sc.add_source_bucket(bucket_3)
    infected_topic = sns.Topic(self, "rInfectedTopic")
    if sc.infected_rule != None:
      sc.infected_rule.add_target(
        events_targets.SnsTopic(
          infected_topic,
          message=events.RuleTargetInput.from_event_path('$.detail.responsePayload.message'),
        )
      )
```

</p>
</details>

### Example 2. (Bring your own destinations)

<details><summary>typescript</summary>
<p>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_lambda_destinations import SqsDestination, EventBridgeDestination
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_sqs import Queue
from aws_cdk.core import Construct, Stack, StackProps
from cdk_serverless_clamscan import ServerlessClamscan

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        bucket_1 = Bucket(self, "rBucket1")
        bucket_2 = Bucket(self, "rBucket2")
        bucket_list = [bucket_1, bucket_2]
        queue = Queue(self, "rQueue")
        sc = ServerlessClamscan(self, "default",
            buckets=bucket_list,
            on_result=EventBridgeDestination(),
            on_error=SqsDestination(queue)
        )
        bucket_3 = Bucket(self, "rBucket3")
        sc.add_source_bucket(bucket_3)
```

</p>
</details><details><summary>python</summary>
<p>

```python
from aws_cdk import (
  core as core,
  aws_lambda_destinations as lambda_destinations,
  aws_s3 as s3,
  aws_sqs as sqs
)
from cdk_serverless_clamscan import ServerlessClamscan

class CdkTestStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    bucket_1 = s3.Bucket(self, "rBucket1")
    bucket_2 = s3.Bucket(self, "rBucket2")
    bucketList = [ bucket_1, bucket_2 ]
    queue = sqs.Queue(self, "rQueue")
    sc = ServerlessClamscan(self, "rClamScan",
      buckets=bucketList,
      on_result=lambda_destinations.EventBridgeDestination(),
      on_error=lambda_destinations.SqsDestination(queue),
    )
    bucket_3 = s3.Bucket(self, "rBucket3")
    sc.add_source_bucket(bucket_3)
```

</p>
</details>

## Operation and Maintenance

When ClamAV publishes updates to the scanner you will see “Your ClamAV installation is OUTDATED” in your scan results. While the construct creates a system to keep the database definitions up to date, you must update the scanner to detect all the latest Viruses.

Update the docker images of the Lambda functions with the latest version of ClamAV by re-running `cdk deploy`.

## API Reference

See [API.md](./API.md).

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md) for more information.

## License

This project is licensed under the Apache-2.0 License.
