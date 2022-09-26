"""Main python file_key for adding resources to the application stack."""
from typing import Dict, Any
import aws_cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

from .vpc_construct import VPCService
from .security_group_construct import SecurityGroupConstruct


class MainProjectStack(aws_cdk.Stack):
    """Build the app stacks and its resources."""
    def __init__(self, env_var: str, scope: Construct, 
                 app_id: str, config: dict, **kwargs: Dict[str, Any]) -> None:
        """Creates the cloudformation templates for the projects."""
        super().__init__(scope, app_id, **kwargs)
        self.env_var = env_var
        self.config = config
        MainProjectStack.create_stack(self, self.env_var, config=config)

    @staticmethod
    def create_stack(stack: aws_cdk.Stack, env: str, config: dict) -> None:
        """Create and add the resources to the application stack"""

        print(env)
        print(config)

        # Import the existing VPN, subnet and create the Securty Group
        MainProjectStack.setup_vpc_and_security(stack)

    @staticmethod
    def setup_vpc_and_security(stack: aws_cdk.Stack) -> None:
        """Import the existing VPN, subnet and create the Securty Group"""

        # Import existing VPC
        existing_vpc = VPCService.import_vpc(stack)

        # Create Security Group for RDS
        rds_security_group = SecurityGroupConstruct.create_rds_security_group(
            stack,
            existing_vpc
        )

        # Create Security Group for Lambda
        lambda_security_group = SecurityGroupConstruct.create_lambda_security_group(
            stack,
            existing_vpc
        )
        print(f"----------- ********* lambda_security_group : {lambda_security_group}")

        # Create Security Group for CodeBuild
        codebuild_security_group = SecurityGroupConstruct.create_codebuild_security_group(
            stack,
            existing_vpc
        )

        codebuild_security_group.connections.allow_to_any_ipv4(
            ec2.Port.tcp(443),
            "Grant Outbound to Github (or anything else.)"
        )

        # Allow connection to RDS for Codebuild
        rds_security_group.connections.allow_from(
            codebuild_security_group,
            ec2.Port.tcp(5432),
            "Allow CodeBuild access to RDS on port 5432"
        )

        # Allow connection to RDS for Api Lambda
        rds_security_group.connections.allow_from(
            lambda_security_group,
            ec2.Port.tcp(5432),
            "Allow Api Lambdas to access RDS on port 5432"
        )     