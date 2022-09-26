"""Main python script for VPC configurations related stuff."""
import aws_cdk
import aws_cdk.aws_ec2 as ec2


class VPCService():
    """Class with static methods that are used to build and deploy VPC."""

    @staticmethod
    def import_vpc(stack: aws_cdk.Stack) -> ec2.Vpc:
        """Method to obtain existing VPC."""
        get_vpc = ec2.Vpc.from_lookup(
            scope=stack,
            id="vpc-09d3f642a4f17a01e",
            is_default=True,
            vpc_name='kk-default-vpc'
        )
        return get_vpc