# OurChants-Backend Architecture Documentation

## Overview

OurChants-Backend is a serverless application for managing song data, built on AWS using the AWS CDK. The application provides a RESTful API for CRUD operations on song data, with data stored in PostgreSQL and assets stored in S3.

## Architecture

### Components

1. **API Layer**
   - AWS API Gateway: Provides RESTful endpoints for song operations
   - AWS Lambda: Handles API requests and business logic
   - Endpoints:
     - GET /songs - List all songs
     - POST /songs - Create new song
     - GET /songs/{id} - Get specific song
     - PUT /songs/{id} - Update song
     - DELETE /songs/{id} - Delete song

2. **Data Layer**
   - Amazon RDS (PostgreSQL): Stores song metadata
   - Amazon S3: Stores song assets (e.g., audio files, album art)
   - AWS Systems Manager Parameter Store: Stores database credentials

3. **Infrastructure**
   - AWS VPC: Network isolation for RDS and Lambda
   - AWS IAM: Access control and permissions
   - AWS CDK: Infrastructure as Code

### Service Justification

- **API Gateway**: Provides scalable, secure API endpoints with built-in request validation and throttling
- **Lambda**: Serverless compute for API handlers, scales automatically with demand
- **RDS (PostgreSQL)**: Relational database for structured song data with ACID compliance
- **S3**: Durable object storage for song assets with versioning and encryption
- **Parameter Store**: Secure storage for sensitive configuration
- **VPC**: Network isolation for security and compliance

## Deployment Guide

### Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI configured with credentials
3. Node.js and npm installed
4. Python 3.8+ installed
5. AWS CDK CLI installed:
   ```bash
   npm install -g aws-cdk
   ```

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ourchants-backend.git
   cd ourchants-backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Bootstrap CDK (first time only):
   ```bash
   cdk bootstrap
   ```

4. Deploy the stack:
   ```bash
   cdk deploy
   ```

### Environment Variables

Create a `.env` file with the following variables:
```
DB_HOST=<RDS endpoint>
DB_NAME=ourchants
DB_PORT=5432
ASSETS_BUCKET=<S3 bucket name>
```

## Testing Guide

### Unit Tests

1. Run data model tests:
   ```bash
   python -m pytest tests/test_song.py
   ```

2. Run infrastructure tests:
   ```bash
   python -m pytest tests/test_infrastructure.py
   ```

### Integration Tests

1. Deploy the stack first
2. Run integration tests:
   ```bash
   python -m pytest tests/test_infrastructure.py -k "not skip"
   ```

### Troubleshooting

#### Database Issues

1. Check RDS connectivity:
   ```bash
   psql -h <RDS endpoint> -U postgres -d ourchants
   ```

2. Verify database schema:
   ```sql
   \dt
   \d songs
   ```

#### API Issues

1. Check API Gateway logs:
   ```bash
   aws logs get-log-events --log-group-name /aws/apigateway/OurChantsAPI
   ```

2. Check Lambda logs:
   ```bash
   aws logs get-log-events --log-group-name /aws/lambda/OurChantsAPIFunction
   ```

#### S3 Issues

1. Verify bucket permissions:
   ```bash
   aws s3api get-bucket-acl --bucket ourchants-assets
   ```

2. Check bucket encryption:
   ```bash
   aws s3api get-bucket-encryption --bucket ourchants-assets
   ```

## Codebase Structure

```
ourchants-backend/
├── infrastructure/          # CDK infrastructure code
│   ├── app_stack.py        # Main stack definition
│   └── database.py         # Database stack
├── models/                 # Data models
│   └── song.py            # Song data model
├── src/                    # Application code
│   └── api/               # Lambda function code
├── tests/                  # Test suite
│   ├── test_song.py       # Data model tests
│   └── test_infrastructure.py # Infrastructure tests
└── docs/                   # Documentation
```

## Component Interactions

1. **API Request Flow**
   - Client → API Gateway → Lambda → RDS/S3
   - Response: S3/RDS → Lambda → API Gateway → Client

2. **Data Flow**
   - Song metadata stored in RDS
   - Song assets stored in S3
   - Database credentials in Parameter Store

3. **Security Flow**
   - VPC isolates RDS and Lambda
   - IAM roles control access
   - S3 encryption for assets
   - Parameter Store for secrets

## Best Practices

1. **Security**
   - Use VPC for network isolation
   - Encrypt sensitive data
   - Follow least privilege principle
   - Rotate credentials regularly

2. **Performance**
   - Use appropriate indexes in RDS
   - Enable S3 transfer acceleration
   - Configure Lambda memory appropriately
   - Use API Gateway caching

3. **Maintenance**
   - Regular database backups
   - Monitor resource usage
   - Update dependencies
   - Review security policies

## Monitoring and Logging

1. **CloudWatch Metrics**
   - API Gateway: 4xx/5xx errors, latency
   - Lambda: Invocations, errors, duration
   - RDS: CPU, memory, connections
   - S3: Requests, errors

2. **CloudWatch Logs**
   - API Gateway access logs
   - Lambda execution logs
   - RDS performance insights

## Scaling Considerations

1. **Horizontal Scaling**
   - Lambda scales automatically
   - API Gateway handles increased traffic
   - RDS read replicas if needed

2. **Vertical Scaling**
   - Increase Lambda memory
   - Upgrade RDS instance
   - Adjust API Gateway throttling

## Cost Optimization

1. **Resource Sizing**
   - Right-size RDS instance
   - Optimize Lambda memory
   - Use S3 lifecycle policies

2. **Architecture**
   - Use serverless where possible
   - Implement caching
   - Optimize database queries

## Disaster Recovery

1. **Backup Strategy**
   - RDS automated backups
   - S3 versioning
   - Infrastructure as Code

2. **Recovery Procedures**
   - Database restore process
   - Infrastructure redeployment
   - Data validation steps 