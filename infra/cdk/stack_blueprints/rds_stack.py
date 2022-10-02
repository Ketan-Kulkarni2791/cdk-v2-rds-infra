"""Main python file_key for adding resources to the application stack."""
from typing import Dict, Any
import aws_cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_s3 as s3
# import aws_cdk.aws_kms as kms
from constructs import Construct

from .vpc_construct import VPCService
from .security_group_construct import SecurityGroupConstruct
from .iam_construct import IAMConstruct
from .kms_construct import KMSConstruct
from .s3_construct import S3Construct
from .ssm_construct import SSMConstruct
from .secret_manager_construct import SecretManagerConstruct
from .rds_construct import RDSConstruct


class RDSStack(aws_cdk.Stack):
    """Build the app stacks and its resources."""
    def __init__(self, env_var: str, scope: Construct, 
                 app_id: str, config: dict, **kwargs: Dict[str, Any]) -> None:
        """Creates the cloudformation templates for the projects."""
        super().__init__(scope, app_id, **kwargs)
        self.env_var = env_var
        self.config = config
        RDSStack.create_stack(self, self.env_var, config=config)

    @staticmethod
    def create_stack(stack: aws_cdk.Stack, env: str, config: dict) -> None:
        """Create and add the resources to the application stack"""

        print(env)
        print(config)

        # Import the existing VPN, subnet and create the Securty Group
        existing_vpc, rds_security_group = RDSStack.setup_vpc_and_security(stack)

        # KMS infra setup ------------------------------------------------------
        kms_pol_doc = IAMConstruct.get_kms_policy_document()

        kms_key = KMSConstruct.create_kms_key(
            stack=stack,
            config=config,
            policy_doc=kms_pol_doc
        )
        print(kms_key)

        # S3 Bucket Infra Setup --------------------------------------------------
        bucketname = RDSStack.create_bucket(
            config=config,
            env=env,
            stack=stack
        )

        # SSM Parameter Construct
        SSMConstruct.create_param(
            stack,
            config,
            "bucket_name",
            bucketname.bucket_name
            # config['global']['bucket_name']
        )
        # SSMConstruct.create_param(
        #     stack,
        #     config,
        #     "kms_key_arn",
        #     kms.Key
        # )

        # Secret Manager Infra
        secret_manager = SecretManagerConstruct.create_secret(stack, config)

        # RDS Database Infra
        rds_db_cluster = RDSConstruct.create_rds(
            stack,
            config,
            existing_vpc,
            rds_security_group,
            secret_manager,
            # kms_key,
            config["global"]["region"]
        )

        # SSM Parameter Construct
        SSMConstruct.create_param(stack, config, "rds_secret_full_arn", secret_manager.secret_full_arn)
        SSMConstruct.create_param(stack, config, "rds_endpoint", rds_db_cluster.attr_endpoint_address)

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

        # Added Secret Manager Endpoint to VPC.
        existing_vpc.add_interface_endpoint(
            "SecretManagerEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER
        )
        # Added Code build Endpoint to VPC.
        existing_vpc.add_interface_endpoint(
            "CodeBuildEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.CODEBUILD
        )
        # Added Athena Endpoint to VPC.
        existing_vpc.add_interface_endpoint(
            "AthenaEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.ATHENA
        )

        return existing_vpc, rds_security_group

    @staticmethod
    def create_bucket(
            config: dict,
            env: str,
            stack: aws_cdk.Stack) -> s3.Bucket:
        """Create an encrypted s3 bucket."""

        print(env)
        s3_bucket = S3Construct.create_bucket(
            stack=stack,
            bucket_id=f"rds-infra-{config['global']['env']}",
            bucket_name=config['global']['bucket_name']
        )
        print(s3_bucket)