"""Main script for adding FlyWay resources."""
from typing import Dict, Any
import aws_cdk
from aws_cdk import Stack
from constructs import Construct
from stack_blueprints.rds_stack import RDSStack

from .ssm_construct import SSMConstruct
from .athena_construct import AthenaConstruct


class FlywayStack(Stack):
    """Build the app stacks and its resources."""
    # pylint: disable=too-many-locals,too-many-arguments
    def __init__(self, env_var: str, scope: Construct, 
                 app_id: str, config: dict, rds_stack: RDSStack, **kwargs: Dict[str, Any]) -> None:
        """Creates the cloudformation templates for the projects."""
        super().__init__(scope, app_id, **kwargs)
        self.env_var = env_var
        self.config = config
        FlywayStack.create_stack(self, self.env_var, config=config, rds_stack=rds_stack)

    @staticmethod
    def create_stack(stack: aws_cdk.Stack, env: str, config: dict, rds_stack: RDSStack) -> None:
        """Create and add the resources to the application stack"""

        print(env)
        print(config)

        rds_secret_arn = SSMConstruct.get_param(stack, config, "rds_secret_full_arn")
        rds_endpoint = SSMConstruct.get_param(stack, config, "rds_endpoint")

        FlywayStack.setup_athena(stack, rds_stack, rds_endpoint, rds_secret_arn)

    @staticmethod
    def setup_athena(stack: aws_cdk.Stack, rds_stack: RDSStack, rds_endpoint, rds_secret_arn):
        """Athena Infra setup."""
        print(rds_stack)
        AthenaConstruct.create_work_group(stack, rds_endpoint, rds_secret_arn)