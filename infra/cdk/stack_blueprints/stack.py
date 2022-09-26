"""Main python file_key for adding resources to the application stack."""
from typing import Dict, Any
import aws_cdk
from constructs import Construct

from .vpc_construct import VPCService


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

        # Import the existing VPN, subnet and create the Securty Group
        MainProjectStack.setup_vpc_and_security(stack)

    @staticmethod
    def setup_vpc_and_security(stack: aws_cdk.Stack) -> None:
        """Import the existing VPN, subnet and create the Securty Group"""

        # Import existing VPC
        existing_vpc = VPCService.import_vpc(stack)
        print(f"--------------- ******* existing_vpc : {existing_vpc}")