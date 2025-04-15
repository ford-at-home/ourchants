import os
import psycopg2
from dotenv import load_dotenv
import pytest

def test_database_connection():
    """Test that we can connect to the database."""
    load_dotenv()
    
    db_params = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME', 'songs'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    conn = psycopg2.connect(**db_params)
    assert conn is not None
    conn.close()

def test_table_exists():
    """Test that the songs table exists and has the correct structure."""
    load_dotenv()
    
    db_params = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME', 'songs'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    
    # Check if table exists
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'songs'
        );
    """)
    assert cur.fetchone()[0], "Songs table does not exist"
    
    # Check table structure
    cur.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'songs'
        ORDER BY ordinal_position;
    """)
    
    columns = cur.fetchall()
    expected_columns = {
        ('id', 'character varying', 'NO'),
        ('name', 'character varying', 'NO'),
        ('artist', 'character varying', 'NO'),
        ('album', 'character varying', 'NO'),
        ('release_date', 'date', 'NO'),
        ('genre', 'character varying', 'NO'),
        ('duration_in_seconds', 'integer', 'NO'),
        ('created_at', 'timestamp with time zone', 'YES'),
        ('updated_at', 'timestamp with time zone', 'YES')
    }
    
    assert set(columns) == expected_columns, "Table structure does not match expected schema"
    
    cur.close()
    conn.close()

def test_sample_data_loaded():
    """Test that the sample data has been loaded correctly."""
    load_dotenv()
    
    db_params = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME', 'songs'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    
    # Check number of records
    cur.execute("SELECT COUNT(*) FROM songs")
    count = cur.fetchone()[0]
    assert count == 10, f"Expected 10 songs, found {count}"
    
    # Check a sample record
    cur.execute("""
        SELECT id, name, artist, album, release_date, genre, duration_in_seconds
        FROM songs
        WHERE id = 'SONG001'
    """)
    song = cur.fetchone()
    
    assert song is not None, "Sample song not found"
    assert song[0] == 'SONG001'
    assert song[1] == 'Midnight Dreams'
    assert song[2] == 'Luna Eclipse'
    assert song[3] == 'Starlight Serenade'
    assert song[4].strftime('%Y-%m-%d') == '2023-03-15'
    assert song[5] == 'Electronic'
    assert song[6] == 245
    
    cur.close()
    conn.close() 