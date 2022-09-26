"""Main python script for Security Group configurations related stuff."""
import aws_cdk
import aws_cdk.aws_ec2 as ec2


class SecurityGroupConstruct:
    """Class with static methods that are used to build and deploy Security Groups."""

    @staticmethod
    def create_rds_security_group(stack: aws_cdk.Stack, vpc: str) -> ec2.SecurityGroup:
        """Method to create Security Group."""
        return ec2.SecurityGroup(
            stack,
            id="RdsInfraRDSSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Basic Setup for creating RDS infra.",
            disable_inline_rules=False
        )