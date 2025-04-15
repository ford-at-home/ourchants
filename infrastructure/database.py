from aws_cdk import (
    Stack,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_secretsmanager as secretsmanager,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct
import string
import random

class DatabaseStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(self, "SongDatabaseVPC")

        # Create security group
        security_group = ec2.SecurityGroup(
            self, "DatabaseSecurityGroup",
            vpc=vpc,
            description="Security group for song database"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(5432),
            "Allow PostgreSQL access"
        )

        # Generate a secure password
        def generate_password():
            chars = string.ascii_letters + string.digits + "!@#$%^&*()"
            return ''.join(random.choice(chars) for _ in range(16))

        # Create a secret for the database password
        db_password = secretsmanager.Secret(
            self, "DatabasePassword",
            description="Password for the song database",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template='{"username": "postgres"}',
                generate_string_key="password",
                password_length=16,
                exclude_characters='"@/\\',
            )
        )

        # Create database instance
        database = rds.DatabaseInstance(
            self, "SongDatabase",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_15
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PUBLIC
            ),
            security_groups=[security_group],
            database_name="songs",
            credentials=rds.Credentials.from_secret(db_password),
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False
        )

        # Output the database connection details
        CfnOutput(
            self, "DatabaseEndpoint",
            value=database.instance_endpoint.hostname,
            description="The endpoint of the database",
            export_name="DatabaseEndpoint"
        )

        CfnOutput(
            self, "DatabasePort",
            value=str(database.instance_endpoint.port),
            description="The port of the database",
            export_name="DatabasePort"
        )

        CfnOutput(
            self, "DatabaseName",
            value="songs",
            description="The name of the database",
            export_name="DatabaseName"
        )

        CfnOutput(
            self, "DatabaseUsername",
            value="postgres",
            description="The username for the database",
            export_name="DatabaseUsername"
        )

        CfnOutput(
            self, "DatabasePasswordSecret",
            value=db_password.secret_name,
            description="The name of the secret containing the database password",
            export_name="DatabasePasswordSecret"
        ) 