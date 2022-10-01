"""Main python file_key for adding resources to the application stack."""
import aws_cdk.aws_athena as aws_athena
from symbol import parameters


class AthenaConstruct:
    """Build the app stacks and its resources."""
    @staticmethod
    def create_data_catalog(stack, parameters):
        return aws_athena.CfnDataCatalog(
            stack,
            id="rds_infra_athena_data_catalog",
            description="Athena data catalog for RDS infra.",
            type="LAMBDA",
            name="rds_infra_athena_data_catalog",
            parameters=parameters
        )

    @staticmethod
    def create_work_group(stack, bucket_name):
        """Work group creation."""
        return aws_athena.CfnWorkGroup(
            stack,
            "rds-infra-work-group",
            name="rds-infra",
            description="Workgroup for RDS Infra.",
            work_group_configuration=aws_athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                result_configuration=aws_athena.CfnWorkGroup.ResultConfigurationProperty(
                    outout_location=f"s3://{bucket_name}",
                    encryption_configuration=aws_athena.CfnWorkGroup.EncryptionConfigurationProperty(
                        encryption_option="SSE_S3"
                    ),
                ),
                enforce_work_group_configuration=True,
            ),
        )
 