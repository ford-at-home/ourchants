import json
import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

def load_sample_data():
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

    # Read sample data
    with open('data/sample_songs.json', 'r') as f:
        data = json.load(f)

    # Connect to database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    try:
        # Insert each song
        for song in data['songs']:
            cur.execute("""
                INSERT INTO songs 
                (id, name, artist, album, release_date, genre, duration_in_seconds)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                song['id'],
                song['name'],
                song['artist'],
                song['album'],
                song['release_date'],
                song['genre'],
                song['duration_in_seconds']
            ))
        
        # Commit the transaction
        conn.commit()
        print(f"Successfully loaded {len(data['songs'])} songs into the database")

    except Exception as e:
        print(f"Error loading data: {e}")
        conn.rollback()
    
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    load_sample_data() 