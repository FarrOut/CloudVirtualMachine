import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="cloud_virtual_machine",
    version="0.0.1",

    description="A CloudVirtualMachine pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Greg Farr",

    package_dir={"": "cloud_virtual_machine"},
    packages=setuptools.find_packages(where="cloud_virtual_machine"),

    install_requires=[
        "aws-cdk.core==1.134.0",
        "aws-cdk.aws_ec2==1.134.0",
        "aws-cdk.pipelines==1.134.0",
        "aws-cdk.aws_secretsmanager==1.134.0",
        "aws-cdk.aws_s3_assets==1.134.0",
        "aws-cdk.aws_s3==1.134.0",
        "aws-cdk.aws_codebuild==1.134.0",
        "aws-cdk.aws_autoscaling==1.134.0",
        "aws-cdk.aws_logs==1.134.0",
        "logging",
        'jsii>=1.44.2',
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
