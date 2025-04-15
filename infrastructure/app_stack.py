from aws_cdk import (
    Stack,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_s3 as s3,
    aws_ssm as ssm,
    RemovalPolicy,
    Duration,
    CfnOutput,
)
from constructs import Construct

class OurChantsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(
            self, "OurChantsVPC",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                ),
                ec2.SubnetConfiguration(
                    name="Isolated",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                ),
            ],
        )

        # Create security group for RDS
        db_security_group = ec2.SecurityGroup(
            self, "DatabaseSecurityGroup",
            vpc=vpc,
            description="Security group for OurChants database",
        )

        # Create RDS instance
        db_instance = rds.DatabaseInstance(
            self, "OurChantsDatabase",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_15
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO,
            ),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            ),
            security_groups=[db_security_group],
            database_name="ourchants",
            removal_policy=RemovalPolicy.DESTROY,
            deletion_protection=False,
            backup_retention=Duration.days(7),
        )

        # Create S3 bucket for assets
        assets_bucket = s3.Bucket(
            self, "OurChantsAssets",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            versioned=True
        )

        # Create Lambda function for API
        api_function = lambda_.Function(
            self, "OurChantsAPIFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="api.handler",
            code=lambda_.Code.from_asset("src/api"),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            security_groups=[db_security_group],
            environment={
                "DB_HOST": db_instance.instance_endpoint.hostname,
                "DB_NAME": "ourchants",
                "DB_PORT": "5432",
                "ASSETS_BUCKET": assets_bucket.bucket_name,
            },
            timeout=Duration.seconds(30),
            memory_size=256,
        )

        # Grant permissions
        db_instance.secret.grant_read(api_function)
        assets_bucket.grant_read_write(api_function)

        # Create API Gateway
        api = apigw.RestApi(
            self, "OurChantsAPIGateway",
            rest_api_name="OurChants API",
            description="API for OurChants application",
            deploy_options=apigw.StageOptions(
                stage_name="prod",
                logging_level=apigw.MethodLoggingLevel.INFO,
                data_trace_enabled=True,
            ),
        )

        # Add API Gateway integration
        api_integration = apigw.LambdaIntegration(api_function)
        
        # Add resources and methods
        songs = api.root.add_resource("songs")
        songs.add_method("GET", api_integration)
        songs.add_method("POST", api_integration)
        
        song = songs.add_resource("{song_id}")
        song.add_method("GET", api_integration)
        song.add_method("PUT", api_integration)
        song.add_method("DELETE", api_integration)

        # Store sensitive data in Parameter Store
        ssm.StringParameter(
            self, "DatabaseSecret",
            parameter_name="/ourchants/database/secret",
            string_value=db_instance.secret.secret_arn,
        )

        # Output important values
        CfnOutput(
            self, "DatabaseEndpoint",
            value=db_instance.instance_endpoint.hostname,
            description="Database endpoint",
        )
        
        CfnOutput(
            self, "APIEndpoint",
            value=api.url,
            description="API endpoint",
        )
        
        CfnOutput(
            self, "AssetsBucket",
            value=assets_bucket.bucket_name,
            description="S3 bucket for assets",
        ) 