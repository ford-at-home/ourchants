import os
import psycopg2
from dotenv import load_dotenv

def setup_database():
    # Load environment variables
    load_dotenv()
    
    # Database connection parameters
    db_params = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME', 'songs'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT', '5432')
    }

    # Read schema file
    with open('infrastructure/schema.sql', 'r') as f:
        schema_sql = f.read()

    # Connect to database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    try:
        # Execute schema SQL
        cur.execute(schema_sql)
        
        # Commit the transaction
        conn.commit()
        print("Successfully created database schema")

    except Exception as e:
        print(f"Error setting up database: {e}")
        conn.rollback()
    
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    setup_database() 