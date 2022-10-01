#!/usr/bin/env python3
from configparser import ConfigParser, ExtendedInterpolation
import aws_cdk as cdk
from stack_blueprints.rds_stack import RDSStack
from stack_blueprints.flyway_stack import FlywayStack


def main() -> None:
    """main.py method that the cdk will execute."""
    config = ConfigParser(interpolation=ExtendedInterpolation())
    config.read("../../.configrc/config.ini")
    app = cdk.App()
    env = app.node.try_get_context("env")
    rds_stack = RDSStack(
        env_var=env,
        scope=app,
        app_id=f"{config['global']['app-id']}-RDS-Stack",
        config=config,
        env={
            "region": config['global']["region"],
            "account": config['global']['awsAccount']
        }
    )
    FlywayStack(
        env_var=env,
        scope=app,
        app_id=f"{config['global']['app-id']}-Flyway-Stack",
        config=config,
        rdsStack=rds_stack,
        env={
            "region": config['global']["region"],
            "account": config['global']['awsAccount']
        }
    )

    app.synth()


main()