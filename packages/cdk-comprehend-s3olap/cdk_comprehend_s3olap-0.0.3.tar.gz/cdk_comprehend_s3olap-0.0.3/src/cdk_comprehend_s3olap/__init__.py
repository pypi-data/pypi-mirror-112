'''
# cdk-comprehend-s3olap

This construct creates the foundation for developers to explore the combination of Amazon S3 Object Lambda and Amazon Comprehend for PII scenarios and it is designed with flexibility, i.e, the developers could tweak arguments via CDK to see how AWS services work and behave.

[![License](https://img.shields.io/badge/License-Apache%202.0-green)](https://opensource.org/licenses/Apache-2.0)
[![Current cdk version](https://img.shields.io/github/package-json/dependency-version/HsiehShuJeng/cdk-comprehend-s3olap/@aws-cdk/core)](https://github.com/aws/aws-cdk)
[![Build](https://github.com/HsiehShuJeng/cdk-comprehend-s3olap/actions/workflows/build.yml/badge.svg)](https://github.com/HsiehShuJeng/cdk-comprehend-s3olap/actions/workflows/build.yml) [![Release](https://github.com/HsiehShuJeng/cdk-comprehend-s3olap/workflows/Release/badge.svg)](https://github.com/HsiehShuJeng/cdk-comprehend-s3olap/actions/workflows/release.yml)
[![Python](https://img.shields.io/pypi/pyversions/cdk-comprehend-s3olap)](https://pypi.org) [![pip](https://img.shields.io/badge/pip%20install-cdk--comprehend--s3olap-blue)](https://pypi.org/project/cdk-comprehend-s3olap/)
[![npm version](https://img.shields.io/npm/v/cdk-comprehend-s3olap)](https://www.npmjs.com/package/cdk-comprehend-s3olap) [![pypi version](https://img.shields.io/pypi/v/cdk-comprehend-s3olap)](https://pypi.org/project/cdk-comprehend-s3olap/) [![Maven](https://img.shields.io/maven-central/v/io.github.hsiehshujeng/cdk-comprehend-s3olap)](https://search.maven.org/search?q=a:cdk-comprehend-s3olap) [![nuget](https://img.shields.io/nuget/v/Comprehend.S3olap)](https://www.nuget.org/packages/Comprehend.S3olap/)

# Table of Contents

* [Serverless Architecture](#serverless-architecture)

  * [Access Control](#access-control)
  * [Redaction](#rerfaction)
* [Introduction](#introduction)
* [Example](#example)

  * [Typescript](#typescript)
  * [Python](#python)
  * [Java](#java)
  * [C#](#c)
* [Some Notes](#some-notes)

# Serverless Architecture

## Access Control

**Data Flow**
![image](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2021/05/07/1-2891.jpg)
*Ram R. and Austin Q., 2021*
**Arhictecture**
![image](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2021/05/07/2-2891.jpg)
*Ram R. and Austin Q., 2021*

## Redaction

![image](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2021/05/07/3-2891.jpg)
*Ram R. and Austin Q., 2021*
![image](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2021/05/07/4-2891.jpg)
*Ram R. and Austin Q., 2021*

# Introduction

The architecture was introduced by **Ram Ramani** and **Austin Quam** and was posted on the AWS Blog as [*Protect PII using Amazon S3 Object Lambda to process and modify data during retrieval*](https://aws.amazon.com/tw/blogs/machine-learning/protect-pii-using-amazon-s3-object-lambda-to-process-and-modify-data-during-retrieval/).
I converted the architecture into a CDK constrcut for 4 programming languages. With this construct, you could manage the properties of IAM roles, the Lambda functions with Amazon Comprehend, and few for the constrcut.
Before deploying the construct via the CDK, you could either places the text files, i.e., those for the access control case and redaction case, under a directory with a specific name as the following or just deploying directly yet you need to upload the text files onto the S3 buckets manually yourself. It's all your choie.

```bash
# For the access control case.
$ cd ${ROOT_DIRECTORY_CDK_APPLICATION}
$ mkdir -p files/access_control
$ curl -o survey-results.txt https://raw.githubusercontent.com/aws-samples/amazon-comprehend-examples/master/s3_object_lambda_pii_protection_blog/access-control/survey-results.txt
$ curl -o innocuous.txt https://raw.githubusercontent.com/aws-samples/amazon-comprehend-examples/master/s3_object_lambda_pii_protection_blog/access-control/innocuous.txt
# For the redaction case.
$ cd ${ROOT_DIRECTORY_CDK_APPLICATION}
$ mkdir -p files/redaction
$ curl -o transcript.txt https://raw.githubusercontent.com/aws-samples/amazon-comprehend-examples/master/s3_object_lambda_pii_protection_blog/redaction/transcript.txt
```

# Example

## Typescript

You could also refer to [here](https://github.com/HsiehShuJeng/cdk-comprehend-s3olap/tree/main/src/demo/typescript).

```bash
$ cdk --init language typescript
$ yarn add cdk-comprehend-s3olap
```

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_comprehend_s3olap import ComprehendS3olab

class TypescriptStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        s3olab = ComprehendS3olab(self, "PiiDemo",
            admin_redaction_lambda_config={
                "mask_character": " ",
                "unsupported_file_handling": "PASS"
            },
            billing_redaction_lambda_config={
                "mask_mode": "REPLACE_WITH_PII_ENTITY_TYPE",
                "pii_entity_types": "AGE,DRIVER_ID,IP_ADDRESS,MAC_ADDRESS,PASSPORT_NUMBER,PASSWORD,SSN"
            },
            cusrt_support_redaction_lambda_config={
                "mask_mode": "REPLACE_WITH_PII_ENTITY_TYPE",
                "pii_entity_types": " BANK_ACCOUNT_NUMBER,BANK_ROUTING,CREDIT_DEBIT_CVV,CREDIT_DEBIT_EXPIRY,CREDIT_DEBIT_NUMBER,SSN"
            }
        )

        cdk.CfnOutput(self, "OPiiAccessControlLambdaArn", value=s3olab.pii_access_conrtol_lambda_arn)
        cdk.CfnOutput(self, "OAdminLambdaArn", value=s3olab.admin_lambda_arn)
        cdk.CfnOutput(self, "OBillingLambdaArn", value=s3olab.billing_lambda_arn)
        cdk.CfnOutput(self, "OCustomerSupportLambdaArn", value=s3olab.customer_support_lambda_arn)
        cdk.CfnOutput(self, "OS3ObjectLambdaGeneralArn", value=s3olab.s3object_lambda_access_control_arn)
        cdk.CfnOutput(self, "OS3ObjectLambdaAdminArn", value=s3olab.s3object_lambda_admin_arn)
        cdk.CfnOutput(self, "OS3ObjectLambdaBillingArn", value=s3olab.s3object_lambda_billing_arn)
        cdk.CfnOutput(self, "OS3ObjectLambdaCustomerSupportArn", value=s3olab.customer_support_lambda_arn)

app = cdk.App()
TypescriptStack(app, "TypescriptStack",
    stack_name="Comprehend-S3olap"
)
```

## Python

TBD

## Java

TBD

## C#

TBD

# Some Notes

1. You should see similar items as the following diagram displays after deploying the constrcut.
   ![image](https://raw.githubusercontent.com/HsiehShuJeng/cdk-comprehend-s3olap/main/images/s3olap_console.png)
2. After creating the foundation with success, you could switch roles that the consrtcut creates for you and see how Amazon S3 Object Lambda works.
   ![image](https://raw.githubusercontent.com/HsiehShuJeng/cdk-comprehend-s3olap/main/images/switch_roles.png)
3. You explore Amazon S3 Object Lambda through the Object Lambda access points and open or download the text files.
4. Lambda code that incorporates with Amazon Comprehend could be see [here](https://github.com/aws-samples/amazon-comprehend-examples/tree/master/s3_object_lambda_pii_protection_blog).
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

import aws_cdk.core


class AccessConrtolLambda(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-comprehend-s3olap.AccessConrtolLambda",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        confidence_threshold: typing.Optional[builtins.str] = None,
        contains_pii_entities_thread_count: typing.Optional[builtins.str] = None,
        default_language_code: typing.Optional[builtins.str] = None,
        document_max_size: typing.Optional[builtins.str] = None,
        document_max_size_contains_pii_entities: typing.Optional[builtins.str] = None,
        is_partial_object_supported: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        max_chars_overlap: typing.Optional[builtins.str] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        publish_cloud_watch_metrics: typing.Optional[builtins.str] = None,
        semantic_version: typing.Optional[builtins.str] = None,
        subsegment_overlapping_tokens: typing.Optional[builtins.str] = None,
        unsupported_file_handling: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param confidence_threshold: The minimum prediction confidence score above which PII classification and detection would be considered as final answer. Valid range (0.5 to 1.0). Default: '0.5'
        :param contains_pii_entities_thread_count: Number of threads to use for calling Comprehend's ContainsPiiEntities API. This controls the number of simultaneous calls that will be made from this Lambda. Default: '20'
        :param default_language_code: Default language of the text to be processed. This code will be used for interacting with Comprehend. Default: 'en'
        :param document_max_size: Default maximum document size (in bytes) that this function can process otherwise will throw exception for too large document size. Default: '102400'
        :param document_max_size_contains_pii_entities: Maximum document size (in bytes) to be used for making calls to Comprehend's ContainsPiiEntities API. Default: '50000'
        :param is_partial_object_supported: Whether to support partial objects or not. Accessing partial object through http headers such byte-range can corrupt the object and/or affect PII detection accuracy. Default: 'false'
        :param log_level: Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: 'INFO'
        :param max_chars_overlap: Maximum characters to overlap among segments of a document in case chunking is needed because of maximum document size limit. Default: '200'
        :param pii_entity_types: List of comma separated PII entity types to be considered for access control. Refer Comprehend's documentation page for list of supported PII entity types. Default: 'ALL'
        :param publish_cloud_watch_metrics: True if publish metrics to Cloudwatch, false otherwise. See README.md for details on CloudWatch metrics. Default: 'true'
        :param semantic_version: The version of the serverless application. Default: '1.0.2'
        :param subsegment_overlapping_tokens: Number of tokens/words to overlap among segments of a document in case chunking is needed because of maximum document size limit. Default: '20'
        :param unsupported_file_handling: Handling logic for Unsupported files. Valid values are PASS and FAIL. Default: 'FAIL'
        '''
        props = AccessConrtolLambdaProps(
            confidence_threshold=confidence_threshold,
            contains_pii_entities_thread_count=contains_pii_entities_thread_count,
            default_language_code=default_language_code,
            document_max_size=document_max_size,
            document_max_size_contains_pii_entities=document_max_size_contains_pii_entities,
            is_partial_object_supported=is_partial_object_supported,
            log_level=log_level,
            max_chars_overlap=max_chars_overlap,
            pii_entity_types=pii_entity_types,
            publish_cloud_watch_metrics=publish_cloud_watch_metrics,
            semantic_version=semantic_version,
            subsegment_overlapping_tokens=subsegment_overlapping_tokens,
            unsupported_file_handling=unsupported_file_handling,
        )

        jsii.create(AccessConrtolLambda, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        '''The name of the underlying resoure in the serverless application.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackName"))


@jsii.data_type(
    jsii_type="cdk-comprehend-s3olap.AccessConrtolLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "confidence_threshold": "confidenceThreshold",
        "contains_pii_entities_thread_count": "containsPiiEntitiesThreadCount",
        "default_language_code": "defaultLanguageCode",
        "document_max_size": "documentMaxSize",
        "document_max_size_contains_pii_entities": "documentMaxSizeContainsPiiEntities",
        "is_partial_object_supported": "isPartialObjectSupported",
        "log_level": "logLevel",
        "max_chars_overlap": "maxCharsOverlap",
        "pii_entity_types": "piiEntityTypes",
        "publish_cloud_watch_metrics": "publishCloudWatchMetrics",
        "semantic_version": "semanticVersion",
        "subsegment_overlapping_tokens": "subsegmentOverlappingTokens",
        "unsupported_file_handling": "unsupportedFileHandling",
    },
)
class AccessConrtolLambdaProps:
    def __init__(
        self,
        *,
        confidence_threshold: typing.Optional[builtins.str] = None,
        contains_pii_entities_thread_count: typing.Optional[builtins.str] = None,
        default_language_code: typing.Optional[builtins.str] = None,
        document_max_size: typing.Optional[builtins.str] = None,
        document_max_size_contains_pii_entities: typing.Optional[builtins.str] = None,
        is_partial_object_supported: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        max_chars_overlap: typing.Optional[builtins.str] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        publish_cloud_watch_metrics: typing.Optional[builtins.str] = None,
        semantic_version: typing.Optional[builtins.str] = None,
        subsegment_overlapping_tokens: typing.Optional[builtins.str] = None,
        unsupported_file_handling: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidence_threshold: The minimum prediction confidence score above which PII classification and detection would be considered as final answer. Valid range (0.5 to 1.0). Default: '0.5'
        :param contains_pii_entities_thread_count: Number of threads to use for calling Comprehend's ContainsPiiEntities API. This controls the number of simultaneous calls that will be made from this Lambda. Default: '20'
        :param default_language_code: Default language of the text to be processed. This code will be used for interacting with Comprehend. Default: 'en'
        :param document_max_size: Default maximum document size (in bytes) that this function can process otherwise will throw exception for too large document size. Default: '102400'
        :param document_max_size_contains_pii_entities: Maximum document size (in bytes) to be used for making calls to Comprehend's ContainsPiiEntities API. Default: '50000'
        :param is_partial_object_supported: Whether to support partial objects or not. Accessing partial object through http headers such byte-range can corrupt the object and/or affect PII detection accuracy. Default: 'false'
        :param log_level: Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: 'INFO'
        :param max_chars_overlap: Maximum characters to overlap among segments of a document in case chunking is needed because of maximum document size limit. Default: '200'
        :param pii_entity_types: List of comma separated PII entity types to be considered for access control. Refer Comprehend's documentation page for list of supported PII entity types. Default: 'ALL'
        :param publish_cloud_watch_metrics: True if publish metrics to Cloudwatch, false otherwise. See README.md for details on CloudWatch metrics. Default: 'true'
        :param semantic_version: The version of the serverless application. Default: '1.0.2'
        :param subsegment_overlapping_tokens: Number of tokens/words to overlap among segments of a document in case chunking is needed because of maximum document size limit. Default: '20'
        :param unsupported_file_handling: Handling logic for Unsupported files. Valid values are PASS and FAIL. Default: 'FAIL'
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if confidence_threshold is not None:
            self._values["confidence_threshold"] = confidence_threshold
        if contains_pii_entities_thread_count is not None:
            self._values["contains_pii_entities_thread_count"] = contains_pii_entities_thread_count
        if default_language_code is not None:
            self._values["default_language_code"] = default_language_code
        if document_max_size is not None:
            self._values["document_max_size"] = document_max_size
        if document_max_size_contains_pii_entities is not None:
            self._values["document_max_size_contains_pii_entities"] = document_max_size_contains_pii_entities
        if is_partial_object_supported is not None:
            self._values["is_partial_object_supported"] = is_partial_object_supported
        if log_level is not None:
            self._values["log_level"] = log_level
        if max_chars_overlap is not None:
            self._values["max_chars_overlap"] = max_chars_overlap
        if pii_entity_types is not None:
            self._values["pii_entity_types"] = pii_entity_types
        if publish_cloud_watch_metrics is not None:
            self._values["publish_cloud_watch_metrics"] = publish_cloud_watch_metrics
        if semantic_version is not None:
            self._values["semantic_version"] = semantic_version
        if subsegment_overlapping_tokens is not None:
            self._values["subsegment_overlapping_tokens"] = subsegment_overlapping_tokens
        if unsupported_file_handling is not None:
            self._values["unsupported_file_handling"] = unsupported_file_handling

    @builtins.property
    def confidence_threshold(self) -> typing.Optional[builtins.str]:
        '''The minimum prediction confidence score above which PII classification and detection would be considered as final answer.

        Valid range (0.5 to 1.0).

        :default: '0.5'
        '''
        result = self._values.get("confidence_threshold")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contains_pii_entities_thread_count(self) -> typing.Optional[builtins.str]:
        '''Number of threads to use for calling Comprehend's ContainsPiiEntities API.

        This controls the number of simultaneous calls that will be made from this Lambda.

        :default: '20'
        '''
        result = self._values.get("contains_pii_entities_thread_count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_language_code(self) -> typing.Optional[builtins.str]:
        '''Default language of the text to be processed.

        This code will be used for interacting with Comprehend.

        :default: 'en'
        '''
        result = self._values.get("default_language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_max_size(self) -> typing.Optional[builtins.str]:
        '''Default maximum document size (in bytes) that this function can process otherwise will throw exception for too large document size.

        :default: '102400'
        '''
        result = self._values.get("document_max_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_max_size_contains_pii_entities(self) -> typing.Optional[builtins.str]:
        '''Maximum document size (in bytes) to be used for making calls to Comprehend's ContainsPiiEntities API.

        :default: '50000'
        '''
        result = self._values.get("document_max_size_contains_pii_entities")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_partial_object_supported(self) -> typing.Optional[builtins.str]:
        '''Whether to support partial objects or not.

        Accessing partial object through http headers such byte-range can corrupt the object and/or affect PII detection accuracy.

        :default: 'false'
        '''
        result = self._values.get("is_partial_object_supported")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc.

        :default: 'INFO'
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_chars_overlap(self) -> typing.Optional[builtins.str]:
        '''Maximum characters to overlap among segments of a document in case chunking is needed because of maximum document size limit.

        :default: '200'
        '''
        result = self._values.get("max_chars_overlap")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pii_entity_types(self) -> typing.Optional[builtins.str]:
        '''List of comma separated PII entity types to be considered for access control.

        Refer Comprehend's documentation page for list of supported PII entity types.

        :default: 'ALL'
        '''
        result = self._values.get("pii_entity_types")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_cloud_watch_metrics(self) -> typing.Optional[builtins.str]:
        '''True if publish metrics to Cloudwatch, false otherwise.

        See README.md for details on CloudWatch metrics.

        :default: 'true'
        '''
        result = self._values.get("publish_cloud_watch_metrics")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def semantic_version(self) -> typing.Optional[builtins.str]:
        '''The version of the serverless application.

        :default: '1.0.2'
        '''
        result = self._values.get("semantic_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subsegment_overlapping_tokens(self) -> typing.Optional[builtins.str]:
        '''Number of tokens/words to overlap among segments of a document in case chunking is needed because of maximum document size limit.

        :default: '20'
        '''
        result = self._values.get("subsegment_overlapping_tokens")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unsupported_file_handling(self) -> typing.Optional[builtins.str]:
        '''Handling logic for Unsupported files.

        Valid values are PASS and FAIL.

        :default: 'FAIL'
        '''
        result = self._values.get("unsupported_file_handling")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessConrtolLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdminRole(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-comprehend-s3olap.AdminRole",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        iam_role_name: typing.Optional[builtins.str] = None,
        object_lambda_access_point_name: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param iam_role_name: The name of the IAM role. Default: 'RedactionAdminRole'
        :param object_lambda_access_point_name: The name of the object Lambda access point, which will be the same as the S3 acceess point for the S3 bucket in the demostration. Default: 'admin-s3olap-call-transcripts-known-pii'
        :param policy_name: The name of the IAM policy for the IAM role. Default: 'admin-role-s3olap-policy'
        '''
        props = AdminRoleProps(
            iam_role_name=iam_role_name,
            object_lambda_access_point_name=object_lambda_access_point_name,
            policy_name=policy_name,
        )

        jsii.create(AdminRole, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of the IAM role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> builtins.str:
        '''The unique string identifying the role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''The name of the IAM role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))


@jsii.data_type(
    jsii_type="cdk-comprehend-s3olap.AdminRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "iam_role_name": "iamRoleName",
        "object_lambda_access_point_name": "objectLambdaAccessPointName",
        "policy_name": "policyName",
    },
)
class AdminRoleProps:
    def __init__(
        self,
        *,
        iam_role_name: typing.Optional[builtins.str] = None,
        object_lambda_access_point_name: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param iam_role_name: The name of the IAM role. Default: 'RedactionAdminRole'
        :param object_lambda_access_point_name: The name of the object Lambda access point, which will be the same as the S3 acceess point for the S3 bucket in the demostration. Default: 'admin-s3olap-call-transcripts-known-pii'
        :param policy_name: The name of the IAM policy for the IAM role. Default: 'admin-role-s3olap-policy'
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if iam_role_name is not None:
            self._values["iam_role_name"] = iam_role_name
        if object_lambda_access_point_name is not None:
            self._values["object_lambda_access_point_name"] = object_lambda_access_point_name
        if policy_name is not None:
            self._values["policy_name"] = policy_name

    @builtins.property
    def iam_role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM role.

        :default: 'RedactionAdminRole'
        '''
        result = self._values.get("iam_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_lambda_access_point_name(self) -> typing.Optional[builtins.str]:
        '''The name of the object Lambda access point, which will be the same as the S3 acceess point for the S3 bucket in the demostration.

        :default: 'admin-s3olap-call-transcripts-known-pii'
        '''
        result = self._values.get("object_lambda_access_point_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM policy for the IAM role.

        :default: 'admin-role-s3olap-policy'
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdminRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BillingRole(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-comprehend-s3olap.BillingRole",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        iam_role_name: typing.Optional[builtins.str] = None,
        object_lambda_access_point_name: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param iam_role_name: The name of the IAM role. Default: 'RedactionAdminRole'
        :param object_lambda_access_point_name: The name of the object Lambda access point, which will be the same as the S3 acceess point for the S3 bucket in the demostration. Default: 'admin-s3olap-call-transcripts-known-pii'
        :param policy_name: The name of the IAM policy for the IAM role. Default: 'admin-role-s3olap-policy'
        '''
        props = AdminRoleProps(
            iam_role_name=iam_role_name,
            object_lambda_access_point_name=object_lambda_access_point_name,
            policy_name=policy_name,
        )

        jsii.create(BillingRole, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of the IAM role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> builtins.str:
        '''The unique string identifying the role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''The name of the IAM role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))


@jsii.data_type(
    jsii_type="cdk-comprehend-s3olap.BillingRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "iam_role_name": "iamRoleName",
        "object_lambda_access_point_name": "objectLambdaAccessPointName",
        "policy_name": "policyName",
    },
)
class BillingRoleProps:
    def __init__(
        self,
        *,
        iam_role_name: typing.Optional[builtins.str] = None,
        object_lambda_access_point_name: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param iam_role_name: The name of the IAM role. Default: 'RedactionBillingRole'
        :param object_lambda_access_point_name: The name of the object Lambda access point, which will be the same as the S3 acceess point for the S3 bucket in the demostration. Default: 'billing-s3olap-call-transcripts-known-pii'
        :param policy_name: The name of the IAM policy for the IAM role. Default: 'billing-role-s3olap-policy'
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if iam_role_name is not None:
            self._values["iam_role_name"] = iam_role_name
        if object_lambda_access_point_name is not None:
            self._values["object_lambda_access_point_name"] = object_lambda_access_point_name
        if policy_name is not None:
            self._values["policy_name"] = policy_name

    @builtins.property
    def iam_role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM role.

        :default: 'RedactionBillingRole'
        '''
        result = self._values.get("iam_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_lambda_access_point_name(self) -> typing.Optional[builtins.str]:
        '''The name of the object Lambda access point, which will be the same as the S3 acceess point for the S3 bucket in the demostration.

        :default: 'billing-s3olap-call-transcripts-known-pii'
        '''
        result = self._values.get("object_lambda_access_point_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM policy for the IAM role.

        :default: 'billing-role-s3olap-policy'
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustSupportRole(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-comprehend-s3olap.CustSupportRole",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        iam_role_name: typing.Optional[builtins.str] = None,
        object_lambda_access_point_name: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param iam_role_name: The name of the IAM role. Default: 'RedactionAdminRole'
        :param object_lambda_access_point_name: The name of the object Lambda access point, which will be the same as the S3 acceess point for the S3 bucket in the demostration. Default: 'admin-s3olap-call-transcripts-known-pii'
        :param policy_name: The name of the IAM policy for the IAM role. Default: 'admin-role-s3olap-policy'
        '''
        props = AdminRoleProps(
            iam_role_name=iam_role_name,
            object_lambda_access_point_name=object_lambda_access_point_name,
            policy_name=policy_name,
        )

        jsii.create(CustSupportRole, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of the IAM role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> builtins.str:
        '''The unique string identifying the role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''The name of the IAM role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))


@jsii.data_type(
    jsii_type="cdk-comprehend-s3olap.CustSupportRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "iam_role_name": "iamRoleName",
        "object_lambda_access_point_name": "objectLambdaAccessPointName",
        "policy_name": "policyName",
    },
)
class CustSupportRoleProps:
    def __init__(
        self,
        *,
        iam_role_name: typing.Optional[builtins.str] = None,
        object_lambda_access_point_name: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param iam_role_name: The name of the IAM role. Default: 'RedactionCustSupportRole'
        :param object_lambda_access_point_name: The name of the object Lambda access point, which will be the same as the S3 acceess point for the S3 bucket in the demostration. Default: 'custsupport-s3olap-call-transcripts-known-pii'
        :param policy_name: The name of the IAM policy for the IAM role. Default: 'customersupport-role-s3olap-policy'
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if iam_role_name is not None:
            self._values["iam_role_name"] = iam_role_name
        if object_lambda_access_point_name is not None:
            self._values["object_lambda_access_point_name"] = object_lambda_access_point_name
        if policy_name is not None:
            self._values["policy_name"] = policy_name

    @builtins.property
    def iam_role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM role.

        :default: 'RedactionCustSupportRole'
        '''
        result = self._values.get("iam_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_lambda_access_point_name(self) -> typing.Optional[builtins.str]:
        '''The name of the object Lambda access point, which will be the same as the S3 acceess point for the S3 bucket in the demostration.

        :default: 'custsupport-s3olap-call-transcripts-known-pii'
        '''
        result = self._values.get("object_lambda_access_point_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM policy for the IAM role.

        :default: 'customersupport-role-s3olap-policy'
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustSupportRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GeneralRole(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-comprehend-s3olap.GeneralRole",
):
    '''The role that you are going to assume (switch role).

    Explores how the S3 Object Lambda works.
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        iam_role_name: typing.Optional[builtins.str] = None,
        object_lambda_access_point_name: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param iam_role_name: The name of the IAM role. Default: 'GeneralRole'
        :param object_lambda_access_point_name: The name of the object Lambda access point, which will be the same as the S3 acceess point for the S3 bucket in the demostration. Default: 'accessctl-s3olap-survey-results-unknown-pii'
        :param policy_name: The name of the IAM policy for the IAM role. Default: 'general-role-s3olap-policy'
        '''
        props = GeneralRoleProps(
            iam_role_name=iam_role_name,
            object_lambda_access_point_name=object_lambda_access_point_name,
            policy_name=policy_name,
        )

        jsii.create(GeneralRole, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of the IAM role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> builtins.str:
        '''The unique string identifying the role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''The name of the IAM role.'''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))


@jsii.data_type(
    jsii_type="cdk-comprehend-s3olap.GeneralRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "iam_role_name": "iamRoleName",
        "object_lambda_access_point_name": "objectLambdaAccessPointName",
        "policy_name": "policyName",
    },
)
class GeneralRoleProps:
    def __init__(
        self,
        *,
        iam_role_name: typing.Optional[builtins.str] = None,
        object_lambda_access_point_name: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param iam_role_name: The name of the IAM role. Default: 'GeneralRole'
        :param object_lambda_access_point_name: The name of the object Lambda access point, which will be the same as the S3 acceess point for the S3 bucket in the demostration. Default: 'accessctl-s3olap-survey-results-unknown-pii'
        :param policy_name: The name of the IAM policy for the IAM role. Default: 'general-role-s3olap-policy'
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if iam_role_name is not None:
            self._values["iam_role_name"] = iam_role_name
        if object_lambda_access_point_name is not None:
            self._values["object_lambda_access_point_name"] = object_lambda_access_point_name
        if policy_name is not None:
            self._values["policy_name"] = policy_name

    @builtins.property
    def iam_role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM role.

        :default: 'GeneralRole'
        '''
        result = self._values.get("iam_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_lambda_access_point_name(self) -> typing.Optional[builtins.str]:
        '''The name of the object Lambda access point, which will be the same as the S3 acceess point for the S3 bucket in the demostration.

        :default: 'accessctl-s3olap-survey-results-unknown-pii'
        '''
        result = self._values.get("object_lambda_access_point_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM policy for the IAM role.

        :default: 'general-role-s3olap-policy'
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GeneralRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RedactionLambda(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-comprehend-s3olap.RedactionLambda",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        confidence_threshold: typing.Optional[builtins.str] = None,
        contains_pii_entities_thread_count: typing.Optional[builtins.str] = None,
        default_language_code: typing.Optional[builtins.str] = None,
        detect_pii_entities_thread_count: typing.Optional[builtins.str] = None,
        document_max_size: typing.Optional[builtins.str] = None,
        document_max_size_contains_pii_entities: typing.Optional[builtins.str] = None,
        document_max_size_detect_pii_entities: typing.Optional[builtins.str] = None,
        is_partial_object_supported: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        mask_character: typing.Optional[builtins.str] = None,
        mask_mode: typing.Optional[builtins.str] = None,
        max_chars_overlap: typing.Optional[builtins.str] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        publish_cloud_watch_metrics: typing.Optional[builtins.str] = None,
        semantic_version: typing.Optional[builtins.str] = None,
        subsegment_overlapping_tokens: typing.Optional[builtins.str] = None,
        unsupported_file_handling: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param confidence_threshold: The minimum prediction confidence score above which PII classification and detection would be considered as final answer. Valid range (0.5 to 1.0). Default: '0.5'
        :param contains_pii_entities_thread_count: Number of threads to use for calling Comprehend's ContainsPiiEntities API. This controls the number of simultaneous calls that will be made from this Lambda. Default: '20'
        :param default_language_code: Default language of the text to be processed. This code will be used for interacting with Comprehend. Default: 'en'
        :param detect_pii_entities_thread_count: Number of threads to use for calling Comprehend's DetectPiiEntities API. This controls the number of simultaneous calls that will be made from this Lambda. Default: '8'
        :param document_max_size: Default maximum document size (in bytes) that this function can process otherwise will throw exception for too large document size. Default: '102400'
        :param document_max_size_contains_pii_entities: Maximum document size (in bytes) to be used for making calls to Comprehend's ContainsPiiEntities API. Default: '50000'
        :param document_max_size_detect_pii_entities: Maximum document size (in bytes) to be used for making calls to Comprehend's DetectPiiEntities API. Default: '5000'
        :param is_partial_object_supported: Whether to support partial objects or not. Accessing partial object through http headers such byte-range can corrupt the object and/or affect PII detection accuracy. Default: 'false'
        :param log_level: Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: 'INFO'
        :param mask_character: A character that replaces each character in the redacted PII entity. Default: '*'
        :param mask_mode: Specifies whether the PII entity is redacted with the mask character or the entity type. Valid values - REPLACE_WITH_PII_ENTITY_TYPE and MASK.
        :param max_chars_overlap: Maximum characters to overlap among segments of a document in case chunking is needed because of maximum document size limit. Default: '200'
        :param pii_entity_types: List of comma separated PII entity types to be considered for redaction. Refer Comprehend's documentation page for list of supported PII entity types. Default: 'ALL'
        :param publish_cloud_watch_metrics: True if publish metrics to Cloudwatch, false otherwise. See README.md for details on CloudWatch metrics. Default: 'true'
        :param semantic_version: The version of the serverless application. Default: '1.0.2'
        :param subsegment_overlapping_tokens: Number of tokens/words to overlap among segments of a document in case chunking is needed because of maximum document size limit. Default: '20'
        :param unsupported_file_handling: Handling logic for Unsupported files. Valid values are PASS and FAIL. Default: 'FAIL'
        '''
        props = RedactionLambdaProps(
            confidence_threshold=confidence_threshold,
            contains_pii_entities_thread_count=contains_pii_entities_thread_count,
            default_language_code=default_language_code,
            detect_pii_entities_thread_count=detect_pii_entities_thread_count,
            document_max_size=document_max_size,
            document_max_size_contains_pii_entities=document_max_size_contains_pii_entities,
            document_max_size_detect_pii_entities=document_max_size_detect_pii_entities,
            is_partial_object_supported=is_partial_object_supported,
            log_level=log_level,
            mask_character=mask_character,
            mask_mode=mask_mode,
            max_chars_overlap=max_chars_overlap,
            pii_entity_types=pii_entity_types,
            publish_cloud_watch_metrics=publish_cloud_watch_metrics,
            semantic_version=semantic_version,
            subsegment_overlapping_tokens=subsegment_overlapping_tokens,
            unsupported_file_handling=unsupported_file_handling,
        )

        jsii.create(RedactionLambda, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        '''The name of the underlying resoure in the serverless application.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackName"))


@jsii.data_type(
    jsii_type="cdk-comprehend-s3olap.RedactionLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "confidence_threshold": "confidenceThreshold",
        "contains_pii_entities_thread_count": "containsPiiEntitiesThreadCount",
        "default_language_code": "defaultLanguageCode",
        "detect_pii_entities_thread_count": "detectPiiEntitiesThreadCount",
        "document_max_size": "documentMaxSize",
        "document_max_size_contains_pii_entities": "documentMaxSizeContainsPiiEntities",
        "document_max_size_detect_pii_entities": "documentMaxSizeDetectPiiEntities",
        "is_partial_object_supported": "isPartialObjectSupported",
        "log_level": "logLevel",
        "mask_character": "maskCharacter",
        "mask_mode": "maskMode",
        "max_chars_overlap": "maxCharsOverlap",
        "pii_entity_types": "piiEntityTypes",
        "publish_cloud_watch_metrics": "publishCloudWatchMetrics",
        "semantic_version": "semanticVersion",
        "subsegment_overlapping_tokens": "subsegmentOverlappingTokens",
        "unsupported_file_handling": "unsupportedFileHandling",
    },
)
class RedactionLambdaProps:
    def __init__(
        self,
        *,
        confidence_threshold: typing.Optional[builtins.str] = None,
        contains_pii_entities_thread_count: typing.Optional[builtins.str] = None,
        default_language_code: typing.Optional[builtins.str] = None,
        detect_pii_entities_thread_count: typing.Optional[builtins.str] = None,
        document_max_size: typing.Optional[builtins.str] = None,
        document_max_size_contains_pii_entities: typing.Optional[builtins.str] = None,
        document_max_size_detect_pii_entities: typing.Optional[builtins.str] = None,
        is_partial_object_supported: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        mask_character: typing.Optional[builtins.str] = None,
        mask_mode: typing.Optional[builtins.str] = None,
        max_chars_overlap: typing.Optional[builtins.str] = None,
        pii_entity_types: typing.Optional[builtins.str] = None,
        publish_cloud_watch_metrics: typing.Optional[builtins.str] = None,
        semantic_version: typing.Optional[builtins.str] = None,
        subsegment_overlapping_tokens: typing.Optional[builtins.str] = None,
        unsupported_file_handling: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param confidence_threshold: The minimum prediction confidence score above which PII classification and detection would be considered as final answer. Valid range (0.5 to 1.0). Default: '0.5'
        :param contains_pii_entities_thread_count: Number of threads to use for calling Comprehend's ContainsPiiEntities API. This controls the number of simultaneous calls that will be made from this Lambda. Default: '20'
        :param default_language_code: Default language of the text to be processed. This code will be used for interacting with Comprehend. Default: 'en'
        :param detect_pii_entities_thread_count: Number of threads to use for calling Comprehend's DetectPiiEntities API. This controls the number of simultaneous calls that will be made from this Lambda. Default: '8'
        :param document_max_size: Default maximum document size (in bytes) that this function can process otherwise will throw exception for too large document size. Default: '102400'
        :param document_max_size_contains_pii_entities: Maximum document size (in bytes) to be used for making calls to Comprehend's ContainsPiiEntities API. Default: '50000'
        :param document_max_size_detect_pii_entities: Maximum document size (in bytes) to be used for making calls to Comprehend's DetectPiiEntities API. Default: '5000'
        :param is_partial_object_supported: Whether to support partial objects or not. Accessing partial object through http headers such byte-range can corrupt the object and/or affect PII detection accuracy. Default: 'false'
        :param log_level: Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc. Default: 'INFO'
        :param mask_character: A character that replaces each character in the redacted PII entity. Default: '*'
        :param mask_mode: Specifies whether the PII entity is redacted with the mask character or the entity type. Valid values - REPLACE_WITH_PII_ENTITY_TYPE and MASK.
        :param max_chars_overlap: Maximum characters to overlap among segments of a document in case chunking is needed because of maximum document size limit. Default: '200'
        :param pii_entity_types: List of comma separated PII entity types to be considered for redaction. Refer Comprehend's documentation page for list of supported PII entity types. Default: 'ALL'
        :param publish_cloud_watch_metrics: True if publish metrics to Cloudwatch, false otherwise. See README.md for details on CloudWatch metrics. Default: 'true'
        :param semantic_version: The version of the serverless application. Default: '1.0.2'
        :param subsegment_overlapping_tokens: Number of tokens/words to overlap among segments of a document in case chunking is needed because of maximum document size limit. Default: '20'
        :param unsupported_file_handling: Handling logic for Unsupported files. Valid values are PASS and FAIL. Default: 'FAIL'
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if confidence_threshold is not None:
            self._values["confidence_threshold"] = confidence_threshold
        if contains_pii_entities_thread_count is not None:
            self._values["contains_pii_entities_thread_count"] = contains_pii_entities_thread_count
        if default_language_code is not None:
            self._values["default_language_code"] = default_language_code
        if detect_pii_entities_thread_count is not None:
            self._values["detect_pii_entities_thread_count"] = detect_pii_entities_thread_count
        if document_max_size is not None:
            self._values["document_max_size"] = document_max_size
        if document_max_size_contains_pii_entities is not None:
            self._values["document_max_size_contains_pii_entities"] = document_max_size_contains_pii_entities
        if document_max_size_detect_pii_entities is not None:
            self._values["document_max_size_detect_pii_entities"] = document_max_size_detect_pii_entities
        if is_partial_object_supported is not None:
            self._values["is_partial_object_supported"] = is_partial_object_supported
        if log_level is not None:
            self._values["log_level"] = log_level
        if mask_character is not None:
            self._values["mask_character"] = mask_character
        if mask_mode is not None:
            self._values["mask_mode"] = mask_mode
        if max_chars_overlap is not None:
            self._values["max_chars_overlap"] = max_chars_overlap
        if pii_entity_types is not None:
            self._values["pii_entity_types"] = pii_entity_types
        if publish_cloud_watch_metrics is not None:
            self._values["publish_cloud_watch_metrics"] = publish_cloud_watch_metrics
        if semantic_version is not None:
            self._values["semantic_version"] = semantic_version
        if subsegment_overlapping_tokens is not None:
            self._values["subsegment_overlapping_tokens"] = subsegment_overlapping_tokens
        if unsupported_file_handling is not None:
            self._values["unsupported_file_handling"] = unsupported_file_handling

    @builtins.property
    def confidence_threshold(self) -> typing.Optional[builtins.str]:
        '''The minimum prediction confidence score above which PII classification and detection would be considered as final answer.

        Valid range (0.5 to 1.0).

        :default: '0.5'
        '''
        result = self._values.get("confidence_threshold")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contains_pii_entities_thread_count(self) -> typing.Optional[builtins.str]:
        '''Number of threads to use for calling Comprehend's ContainsPiiEntities API.

        This controls the number of simultaneous calls that will be made from this Lambda.

        :default: '20'
        '''
        result = self._values.get("contains_pii_entities_thread_count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_language_code(self) -> typing.Optional[builtins.str]:
        '''Default language of the text to be processed.

        This code will be used for interacting with Comprehend.

        :default: 'en'
        '''
        result = self._values.get("default_language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detect_pii_entities_thread_count(self) -> typing.Optional[builtins.str]:
        '''Number of threads to use for calling Comprehend's DetectPiiEntities API.

        This controls the number of simultaneous calls that will be made from this Lambda.

        :default: '8'
        '''
        result = self._values.get("detect_pii_entities_thread_count")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_max_size(self) -> typing.Optional[builtins.str]:
        '''Default maximum document size (in bytes) that this function can process otherwise will throw exception for too large document size.

        :default: '102400'
        '''
        result = self._values.get("document_max_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_max_size_contains_pii_entities(self) -> typing.Optional[builtins.str]:
        '''Maximum document size (in bytes) to be used for making calls to Comprehend's ContainsPiiEntities API.

        :default: '50000'
        '''
        result = self._values.get("document_max_size_contains_pii_entities")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_max_size_detect_pii_entities(self) -> typing.Optional[builtins.str]:
        '''Maximum document size (in bytes) to be used for making calls to Comprehend's DetectPiiEntities API.

        :default: '5000'
        '''
        result = self._values.get("document_max_size_detect_pii_entities")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_partial_object_supported(self) -> typing.Optional[builtins.str]:
        '''Whether to support partial objects or not.

        Accessing partial object through http headers such byte-range can corrupt the object and/or affect PII detection accuracy.

        :default: 'false'
        '''
        result = self._values.get("is_partial_object_supported")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''Log level for Lambda function logging, e.g., ERROR, INFO, DEBUG, etc.

        :default: 'INFO'
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mask_character(self) -> typing.Optional[builtins.str]:
        '''A character that replaces each character in the redacted PII entity.

        :default: '*'
        '''
        result = self._values.get("mask_character")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mask_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the PII entity is redacted with the mask character or the entity type.

        Valid values - REPLACE_WITH_PII_ENTITY_TYPE and MASK.

        :fefault: 'MASK'
        '''
        result = self._values.get("mask_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_chars_overlap(self) -> typing.Optional[builtins.str]:
        '''Maximum characters to overlap among segments of a document in case chunking is needed because of maximum document size limit.

        :default: '200'
        '''
        result = self._values.get("max_chars_overlap")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pii_entity_types(self) -> typing.Optional[builtins.str]:
        '''List of comma separated PII entity types to be considered for redaction.

        Refer Comprehend's documentation page for list of supported PII entity types.

        :default: 'ALL'
        '''
        result = self._values.get("pii_entity_types")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_cloud_watch_metrics(self) -> typing.Optional[builtins.str]:
        '''True if publish metrics to Cloudwatch, false otherwise.

        See README.md for details on CloudWatch metrics.

        :default: 'true'
        '''
        result = self._values.get("publish_cloud_watch_metrics")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def semantic_version(self) -> typing.Optional[builtins.str]:
        '''The version of the serverless application.

        :default: '1.0.2'
        '''
        result = self._values.get("semantic_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subsegment_overlapping_tokens(self) -> typing.Optional[builtins.str]:
        '''Number of tokens/words to overlap among segments of a document in case chunking is needed because of maximum document size limit.

        :default: '20'
        '''
        result = self._values.get("subsegment_overlapping_tokens")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def unsupported_file_handling(self) -> typing.Optional[builtins.str]:
        '''Handling logic for Unsupported files.

        Valid values are PASS and FAIL.

        :default: 'FAIL'
        '''
        result = self._values.get("unsupported_file_handling")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RedactionLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccessConrtolLambda",
    "AccessConrtolLambdaProps",
    "AdminRole",
    "AdminRoleProps",
    "BillingRole",
    "BillingRoleProps",
    "CustSupportRole",
    "CustSupportRoleProps",
    "GeneralRole",
    "GeneralRoleProps",
    "RedactionLambda",
    "RedactionLambdaProps",
]

publication.publish()
