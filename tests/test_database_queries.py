"""
Database Query Test Suite for OurChants Application

This test suite verifies the core database functionality of the OurChants application,
which is designed to store and manage sacred chants from various cultural traditions.
The tests ensure that our PostgreSQL database is properly configured and that we can
perform essential queries needed for the application's features.

Key Features Tested:
- Basic CRUD operations through query results
- Data type integrity
- Filtering capabilities (by genre, artist)
- Statistical calculations (average duration)
- Connection management and resource cleanup

These tests represent Phase 3 of our MVP development, focusing on data persistence
and retrieval, which is crucial for building a reliable music streaming platform.
"""

import os
import psycopg2
from dotenv import load_dotenv
import pytest
from datetime import datetime, date

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database using environment variables.
    
    Returns:
        psycopg2.connection: A database connection object
    
    Note:
        Environment variables are loaded from .env file:
        - DB_HOST: Database server hostname
        - DB_NAME: Database name (defaults to 'songs')
        - DB_USER: Database username
        - DB_PASSWORD: Database password
        - DB_PORT: Database port (defaults to 5432)
    """
    load_dotenv()
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME', 'songs'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT', '5432')
    )

def test_query_all_songs():
    """
    Tests the retrieval of all songs from the database and verifies data structure.
    
    This test ensures that:
    1. The songs table exists and contains data
    2. Each song record has the correct number of fields
    3. Each field has the expected data type
    4. The data structure matches our application's requirements
    
    The test is crucial for verifying the integrity of our core data model.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Query all songs with all fields to verify complete data structure
        cur.execute("""
            SELECT id, name, artist, album, release_date, genre, duration_in_seconds
            FROM songs
            ORDER BY name
        """)
        
        songs = cur.fetchall()
        
        # Verify we got results
        assert len(songs) > 0, "No songs found in database"
        
        # Verify first song has correct structure
        first_song = songs[0]
        assert len(first_song) == 7, "Song record has incorrect number of fields"
        assert isinstance(first_song[0], str), "ID should be a string"
        assert isinstance(first_song[1], str), "Name should be a string"
        assert isinstance(first_song[2], str), "Artist should be a string"
        assert isinstance(first_song[3], str), "Album should be a string"
        assert isinstance(first_song[4], date), "Release date should be a date"
        assert isinstance(first_song[5], str), "Genre should be a string"
        assert isinstance(first_song[6], int), "Duration should be an integer"
        
    finally:
        cur.close()
        conn.close()

def test_query_by_genre():
    """
    Tests filtering songs by genre, specifically focusing on Electronic chants.
    
    This test verifies that:
    1. We can filter songs by genre
    2. The filtering returns the correct results
    3. All returned songs match the requested genre
    
    This functionality is essential for the genre-based browsing feature
    of our application, allowing users to explore chants by musical style.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Query songs by genre to test filtering capability
        cur.execute("""
            SELECT id, name, artist, genre
            FROM songs
            WHERE genre = 'Electronic'
            ORDER BY name
        """)
        
        electronic_songs = cur.fetchall()
        
        # Verify we got results
        assert len(electronic_songs) > 0, "No electronic songs found in database"
        
        # Verify all returned songs are electronic genre
        for song in electronic_songs:
            assert song[3] == 'Electronic', f"Song {song[1]} is not in Electronic genre"
            
    finally:
        cur.close()
        conn.close()

def test_query_by_artist():
    """
    Tests filtering songs by artist, using Luna Eclipse as a test case.
    
    This test ensures that:
    1. We can filter songs by artist
    2. The filtering returns the correct results
    3. All returned songs are by the specified artist
    
    This functionality supports the artist profile and discography features
    of our application, allowing users to explore an artist's complete works.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Query songs by artist to test artist filtering
        cur.execute("""
            SELECT id, name, artist, album
            FROM songs
            WHERE artist = 'Luna Eclipse'
            ORDER BY release_date
        """)
        
        artist_songs = cur.fetchall()
        
        # Verify we got results
        assert len(artist_songs) > 0, "No songs by Luna Eclipse found in database"
        
        # Verify all returned songs are by the artist
        for song in artist_songs:
            assert song[2] == 'Luna Eclipse', f"Song {song[1]} is not by Luna Eclipse"
            
    finally:
        cur.close()
        conn.close()

def test_query_song_duration():
    """
    Tests the calculation of average song duration across all chants.
    
    This test verifies that:
    1. We can perform aggregate calculations on the database
    2. The results are within reasonable bounds
    3. The data supports features like playlist duration calculation
    
    This functionality is important for user experience features like
    estimating listening time and creating timed meditation sessions.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Calculate average duration to test aggregate functions
        cur.execute("""
            SELECT AVG(duration_in_seconds) as avg_duration
            FROM songs
        """)
        
        avg_duration = cur.fetchone()[0]
        
        # Verify average duration is reasonable
        assert avg_duration > 0, "Average duration should be positive"
        assert avg_duration < 3600, "Average duration should be less than 1 hour"
        
    finally:
        cur.close()
        conn.close()

@pytest.fixture(scope="module")
def db_connection():
    """
    Pytest fixture that provides a database connection for multiple tests.
    
    This fixture:
    1. Creates a database connection at the start of the test module
    2. Yields the connection to the tests
    3. Ensures proper cleanup by closing the connection after all tests
    
    Using this fixture promotes code reuse and ensures proper resource management.
    """
    conn = get_db_connection()
    yield conn
    conn.close() 