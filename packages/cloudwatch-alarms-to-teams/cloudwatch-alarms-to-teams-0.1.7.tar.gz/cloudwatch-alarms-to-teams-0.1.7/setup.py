import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloudwatch-alarms-to-teams",
    "version": "0.1.7",
    "description": "cloudwatch-alarms-to-teams",
    "license": "Apache-2.0",
    "url": "https://github.com/1davidmichael/Cloudwatch-Alarms-to-Chat-Platforms",
    "long_description_content_type": "text/markdown",
    "author": "David Michael<1.david.michael@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/1davidmichael/Cloudwatch-Alarms-to-Chat-Platforms"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cloudwatch_alarms_to_teams",
        "cloudwatch_alarms_to_teams._jsii"
    ],
    "package_data": {
        "cloudwatch_alarms_to_teams._jsii": [
            "cloudwatch-alarms-to-teams@0.1.7.jsii.tgz"
        ],
        "cloudwatch_alarms_to_teams": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-cloudwatch-actions>=1.113.0, <2.0.0",
        "aws-cdk.aws-cloudwatch>=1.113.0, <2.0.0",
        "aws-cdk.aws-lambda-event-sources>=1.113.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.113.0, <2.0.0",
        "aws-cdk.aws-sns>=1.113.0, <2.0.0",
        "aws-cdk.core>=1.113.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.30.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
