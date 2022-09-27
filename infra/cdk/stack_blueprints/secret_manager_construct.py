"""Code to generate Secret Manager stuff."""
import json
import aws_cdk
import aws_cdk.aws_secretsmanager as sm


class SecretManagerConstruct:
    """Static methods to create Secret Manager."""

    @staticmethod
    def create_secret(stack: aws_cdk.Stack, config: dict) -> sm.Secret:
        """Method to create Secret Manager."""
        secret_string_generator = sm.SecretStringGenerator(
            secret_string_template=json.dumps(
                {
                    "username": "postgres",
                    "db_name": "rdsinfradb",
                    "db_port": "5432"
                }
            ),
            generate_string_key="password",
            password_length=16,
            exclude_characters='@/"`~!#$%^&*}{[](),;:.<>',
            include_space=False,
            exclude_punctuation=True
        )
        secret = sm.Secret(
            scope=stack,
            id=f"{config['global']['appNameShort']}-rds-global-secret",
            description="RDS Infra Setup RDS Username/Password",
            generate_secret_string=secret_string_generator
        )
        return secret