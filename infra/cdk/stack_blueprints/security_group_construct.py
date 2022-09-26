"""Main python script for Security Group configurations related stuff."""
import aws_cdk
import aws_cdk.aws_ec2 as ec2


class SecurityGroupConstruct:
    """Class with static methods that are used to build and deploy Security Groups."""

    @staticmethod
    def create_rds_security_group(stack: aws_cdk.Stack, vpc: str) -> ec2.SecurityGroup:
        """Method to create Security Group for RDS."""
        return ec2.SecurityGroup(
            stack,
            id="RdsInfraRDSSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security group for RDS Database.",
            disable_inline_rules=False
        )

    @staticmethod
    def create_lambda_security_group(stack: aws_cdk.Stack, vpc: str) -> ec2.SecurityGroup:
        """Method to create Security Group for Lambda."""
        return ec2.SecurityGroup(
            stack,
            id="RdsInfraLambdaSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security group for Api Lambda.",
            disable_inline_rules=False
        )

    @staticmethod
    def create_CodeBuild_security_group(stack: aws_cdk.Stack, vpc: str) -> ec2.SecurityGroup:
        """Method to create Security Group for CodeBuild."""
        return ec2.SecurityGroup(
            stack,
            id="RdsInfraCodeBuildSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Allow client access to RDS.",
            disable_inline_rules=False
        )