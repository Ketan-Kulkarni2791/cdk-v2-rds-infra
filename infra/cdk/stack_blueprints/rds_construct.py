"""Code to create RDS Database and other related infra."""
import aws_cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds
# import aws_cdk.aws_kms as kms
import aws_cdk.aws_secretsmanager as sm


class RDSConstruct:
    """Static methods to create RDS Db."""

    #pylint: disable=too-many-arguments
    @staticmethod
    def create_rds(
            stack: aws_cdk.Stack,
            config: dict,
            vpc: ec2.Vpc,
            rds_security_group: ec2.SecurityGroup,
            secret: sm.Secret,
            # kms_key: kms.CfnKey,
            region: str) -> rds.CfnDBCluster:
        """Method to create RDS Db."""
        print(region)
        db_password = secret.secret_value_from_json("password").to_string()
        db_username = secret.secret_value_from_json("username").to_string()
        db_subnet = rds.SubnetGroup(
            scope=stack,
            id=f"{config['global']['appNameShort']}-rds-subnet-group",
            subnet_group_name=f"{config['global']['appNameShort']}-rds-subnet-group",
            description="RDS Infra rds DB cluster subnet group",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnets=[
                        ec2.Subnet.from_subnet_id(stack, "datatier_subnet_az1", config["global"]["subnet1_id"]),
                        ec2.Subnet.from_subnet_id(stack, "datatier_subnet_az2", config["global"]["subnet2_id"])
                ]
            )
        )
        # db_cluster_parameter_grp = rds.CfnDBClusterParameterGroup(
        #     scope=stack,
        #     id=f"{config['global']['appNameShort']}-rds-cluster-parameter-group",
        #     family="default.aurora-postgresql13",
        #     parameters={"rds.force_ssl": "1"},
        #     description="RDS Infra Setup rds db cluster parameter group"
        # )
        global_cluster = rds.CfnGlobalCluster(
            scope=stack,
            id=f"{config['global']['appNameShort']}-rds-global-cluster",
            global_cluster_identifier=f"{config['global']['appNameShort']}-rds-global-cluster",
            source_db_cluster_identifier=f"{config['global']['appNameShort']}-rds-primary-cluster"
        )
        rds_db_instance = rds.CfnDBInstance(
            scope=stack,
            id=f"{config['global']['appNameShort']}-rds-primary-instance",
            db_instance_class="db.r5.large",
            db_cluster_identifier=f"{config['global']['appNameShort']}-rds-primary-cluster",
            db_instance_identifier=f"{config['global']['appNameShort']}-rds-primary-instance",
            db_parameter_group_name="default.aurora-postgresql13",
            db_subnet_group_name=db_subnet.subnet_group_name,
            engine="aurora-postgresql",
            engine_version="13.6",
            monitoring_interval=0,
            auto_minor_version_upgrade=True,
            publicly_accessible=False,
            enable_performance_insights=True,
            performance_insights_retention_period=7
        )
        global_cluster.add_depends_on(rds_db_instance)
        rds_db_cluster = (
            rds.CfnDBCluster(
                scope=stack,
                id="rdsinfrasetuprds",
                # backeup_retention_period=20,
                database_name="rdsinfradatabase",
                db_cluster_identifier=f"{config['global']['appNameShort']}-rds-primary-cluster",
                # db_cluster_parameter_group_name=db_cluster_parameter_grp.ref,
                port=5432,
                db_subnet_group_name=db_subnet.subnet_group_name,
                engine="aurora-postgresql",
                engine_version="13.6",
                # kms_key_id=kms_key.attr_key_id,
                master_username=db_username,
                master_user_password=db_password,
                vpc_security_group_ids=[rds_security_group.security_group_id],
                storage_encrypted=True,
                enable_http_endpoint=True
            )
        )
        rds_db_instance.add_depends_on(rds_db_cluster)
        rds_db_cluster.node.add_dependency(db_subnet)
        return rds_db_cluster