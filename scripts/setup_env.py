#!/usr/bin/env python3
"""
Script to set up environment variables for the OurChants application.
This script retrieves database credentials from AWS CDK stack outputs and creates a minimal .env file.
"""

import boto3
import json
import os
from pathlib import Path

def get_database_credentials():
    """Retrieve database credentials from AWS CDK stack outputs."""
    # Initialize AWS clients
    cloudformation = boto3.client('cloudformation')
    secretsmanager = boto3.client('secretsmanager')
    
    # Get stack outputs
    stack_name = 'SongDatabaseStack'
    try:
        response = cloudformation.describe_stacks(StackName=stack_name)
        outputs = response['Stacks'][0]['Outputs']
        
        # Extract values from outputs
        credentials = {}
        for output in outputs:
            if output['OutputKey'] == 'DatabaseEndpoint':
                credentials['DB_HOST'] = output['OutputValue']
            elif output['OutputKey'] == 'DatabasePort':
                credentials['DB_PORT'] = output['OutputValue']
            elif output['OutputKey'] == 'DatabaseName':
                credentials['DB_NAME'] = output['OutputValue']
            elif output['OutputKey'] == 'DatabaseUsername':
                credentials['DB_USER'] = output['OutputValue']
            elif output['OutputKey'] == 'DatabasePasswordSecret':
                secret_name = output['OutputValue']

        # Get password from secrets manager
        secret_response = secretsmanager.get_secret_value(SecretId=secret_name)
        secret_string = json.loads(secret_response['SecretString'])
        credentials['DB_PASSWORD'] = secret_string['password']

        return credentials
    except Exception as e:
        print(f"Error getting stack outputs: {str(e)}")
        print("Stack outputs:", outputs if 'outputs' in locals() else "No outputs found")
        raise

def create_env_file(credentials):
    """Create a minimal .env file with only database credentials."""
    env_path = Path('.env')
    
    # Check if .env already exists
    if env_path.exists():
        print("Warning: .env file already exists. Please backup and remove it before running this script.")
        return
    
    # Create .env file with only database credentials
    with open('.env', 'w') as f:
        f.write("# Database Configuration\n")
        f.write(f"DB_HOST={credentials['DB_HOST']}\n")
        f.write(f"DB_NAME={credentials['DB_NAME']}\n")
        f.write(f"DB_USER={credentials['DB_USER']}\n")
        f.write(f"DB_PASSWORD={credentials['DB_PASSWORD']}\n")
        f.write(f"DB_PORT={credentials['DB_PORT']}\n")
    
    print("\n.env file created successfully with database credentials.")
    print("Remember to add .env to your .gitignore file!")

def main():
    try:
        print("Retrieving database credentials from AWS CDK stack...")
        credentials = get_database_credentials()
        
        print("Creating .env file...")
        create_env_file(credentials)
        
        print("Successfully created .env file with database credentials!")
        print("\nDatabase connection details:")
        print(f"Host: {credentials['DB_HOST']}")
        print(f"Port: {credentials['DB_PORT']}")
        print(f"Database: {credentials['DB_NAME']}")
        print(f"Username: {credentials['DB_USER']}")
        print("Password: ********")  # Don't print the actual password
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Make sure you have:")
        print("1. Deployed the CDK stack")
        print("2. Configured AWS credentials")
        print("3. Have the necessary AWS permissions")

if __name__ == "__main__":
    main() 