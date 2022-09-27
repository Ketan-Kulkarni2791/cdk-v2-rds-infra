"""Code for generation and deployment of SSM stuff."""
import aws_cdk
import aws_cdk.aws_ssm as aws_ssm


class SSMConstruct:
    """Static methods to create SSM stuff."""

    @staticmethod
    def create_param(stack: aws_cdk.Stack, config: dict, param_name: str, value: str) -> str:
        """Method to create param."""
        name = f"{config['global']['appNameShort']}-{param_name.replace('_', '-')}-{config['global']['env']}"
        return aws_ssm.StringParameter(
            scope=stack,
            id=f"{name}-param",
            parameter_name=name,
            string_value=value
        )

    @staticmethod
    def get_param(stack: aws_cdk.Stack, config: dict, param_name: str) -> str:
        """Method to get param."""
        name = f"{config['global']['appNameShort']}-{param_name.replace('_', '-')}-{config['global']['env']}"
        return aws_ssm.StringParameter.value_for_string_parameter(
            scope=stack,
            parameter_name=name
        )