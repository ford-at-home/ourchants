import boto3
import json
import os
from dotenv import load_dotenv

def get_database_credentials():
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

def update_env_file(credentials):
    # Load existing .env file if it exists
    env_path = '.env'
    if os.path.exists(env_path):
        load_dotenv(env_path)
        existing_vars = {key: os.getenv(key) for key in os.environ}
        # Update with new credentials
        existing_vars.update(credentials)
        credentials = existing_vars

    # Write to .env file
    with open(env_path, 'w') as f:
        for key, value in credentials.items():
            f.write(f"{key}={value}\n")

def main():
    try:
        print("Retrieving database credentials...")
        credentials = get_database_credentials()
        
        print("Updating .env file...")
        update_env_file(credentials)
        
        print("Successfully updated .env file with database credentials!")
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