#!/usr/bin/env python3
"""
Script to verify database connection settings and test the connection.
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

def verify_env_vars():
    """Verify that all required environment variables are set."""
    required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_PORT']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
    
    # Print the database name we're trying to connect to
    print(f"\nAttempting to connect to database: {os.getenv('DB_NAME')}")
    return True

def test_connection():
    """Test the database connection."""
    try:
        # Get connection parameters
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_port = os.getenv('DB_PORT')

        print(f"\nConnection parameters:")
        print(f"Host: {db_host}")
        print(f"Database: {db_name}")
        print(f"User: {db_user}")
        print(f"Port: {db_port}")

        # Attempt connection
        print("\nAttempting to connect...")
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        
        # Test the connection
        with conn.cursor() as cur:
            cur.execute("SELECT current_database();")
            db_name = cur.fetchone()[0]
            print(f"\nSuccessfully connected to database: {db_name}")
        
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        print(f"\nError connecting to database: {str(e)}")
        if "database" in str(e).lower():
            print("\nPossible solutions:")
            print("1. Verify the database name in your .env file")
            print("2. Ensure the database exists on the server")
            print("3. Check your database permissions")
        return False
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        return False

def main():
    """Main function to verify database connection."""
    # Load environment variables from .env file
    load_dotenv()
    
    print("Verifying database connection settings...")
    
    # Verify environment variables
    if not verify_env_vars():
        sys.exit(1)
    
    # Test database connection
    if not test_connection():
        sys.exit(1)
    
    print("\nDatabase connection verified successfully!")

if __name__ == "__main__":
    main() 