#!/usr/bin/env python3
"""
Test suite for database operations module.
Tests CRUD operations and error handling for song data.
"""

import os
import pytest
from datetime import date
from dotenv import load_dotenv
from src.database.operations import (
    Song,
    create_song,
    get_song,
    update_song,
    delete_song,
    list_songs,
    DatabaseError,
    SongNotFoundError,
    InvalidDataError,
    get_db_connection
)

def pytest_configure():
    """Configure pytest and verify database connection settings."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Verify required environment variables are set
    required_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_PORT']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        pytest.exit(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Verify database connection
    try:
        conn = get_db_connection()
        conn.close()
    except Exception as e:
        pytest.exit(f"Failed to connect to database: {str(e)}")

@pytest.fixture(scope="session")
def db_connection():
    """Fixture providing a database connection for tests."""
    # Load environment variables
    load_dotenv()
    
    # Get connection
    conn = get_db_connection()
    yield conn
    conn.close()

@pytest.fixture
def sample_song_data():
    """Fixture providing sample song data for tests."""
    return {
        'id': 'test-song-1',
        'name': 'Test Song',
        'artist': 'Test Artist',
        'album': 'Test Album',
        'release_date': date(2023, 1, 1),
        'genre': 'Test Genre',
        'duration_in_seconds': 180
    }

def test_create_song(db_connection, sample_song_data):
    """Test creating a new song."""
    # Create the song
    song = create_song(sample_song_data)
    
    # Verify the created song
    assert isinstance(song, Song)
    assert song.id == sample_song_data['id']
    assert song.name == sample_song_data['name']
    assert song.artist == sample_song_data['artist']
    assert song.album == sample_song_data['album']
    assert song.release_date == sample_song_data['release_date']
    assert song.genre == sample_song_data['genre']
    assert song.duration_in_seconds == sample_song_data['duration_in_seconds']
    
    # Clean up
    delete_song(song.id)

def test_create_song_invalid_data(db_connection, sample_song_data):
    """Test creating a song with invalid data."""
    # Test missing required field
    invalid_data = sample_song_data.copy()
    del invalid_data['name']
    with pytest.raises(InvalidDataError):
        create_song(invalid_data)
    
    # Test invalid duration
    invalid_data = sample_song_data.copy()
    invalid_data['duration_in_seconds'] = -1
    with pytest.raises(InvalidDataError):
        create_song(invalid_data)

def test_get_song(db_connection, sample_song_data):
    """Test retrieving a song by ID."""
    # Create a song first
    created_song = create_song(sample_song_data)
    
    # Retrieve the song
    retrieved_song = get_song(created_song.id)
    
    # Verify the retrieved song
    assert isinstance(retrieved_song, Song)
    assert retrieved_song.id == created_song.id
    assert retrieved_song.name == created_song.name
    
    # Clean up
    delete_song(created_song.id)

def test_get_song_not_found(db_connection):
    """Test retrieving a non-existent song."""
    with pytest.raises(SongNotFoundError):
        get_song('non-existent-id')

def test_update_song(db_connection, sample_song_data):
    """Test updating a song."""
    # Create a song first
    created_song = create_song(sample_song_data)
    
    # Update the song
    update_data = {
        'name': 'Updated Name',
        'genre': 'Updated Genre'
    }
    updated_song = update_song(created_song.id, update_data)
    
    # Verify the update
    assert updated_song.name == update_data['name']
    assert updated_song.genre == update_data['genre']
    assert updated_song.artist == created_song.artist  # Unchanged field
    
    # Clean up
    delete_song(created_song.id)

def test_update_song_invalid_data(db_connection, sample_song_data):
    """Test updating a song with invalid data."""
    # Create a song first
    created_song = create_song(sample_song_data)
    
    # Test invalid duration
    with pytest.raises(InvalidDataError):
        update_song(created_song.id, {'duration_in_seconds': -1})
    
    # Test empty update data
    with pytest.raises(InvalidDataError):
        update_song(created_song.id, {})
    
    # Clean up
    delete_song(created_song.id)

def test_update_song_not_found(db_connection):
    """Test updating a non-existent song."""
    with pytest.raises(SongNotFoundError):
        update_song('non-existent-id', {'name': 'New Name'})

def test_delete_song(db_connection, sample_song_data):
    """Test deleting a song."""
    # Create a song first
    created_song = create_song(sample_song_data)
    
    # Delete the song
    result = delete_song(created_song.id)
    assert result is True
    
    # Verify the song is deleted
    with pytest.raises(SongNotFoundError):
        get_song(created_song.id)

def test_delete_song_not_found(db_connection):
    """Test deleting a non-existent song."""
    result = delete_song('non-existent-id')
    assert result is False

def test_list_songs(db_connection, sample_song_data):
    """Test listing songs with filtering."""
    # Create multiple songs
    songs = []
    for i in range(3):
        song_data = sample_song_data.copy()
        song_data['id'] = f'test-song-{i}'
        song_data['genre'] = 'Test Genre' if i < 2 else 'Other Genre'
        songs.append(create_song(song_data))
    
    try:
        # Test listing all songs
        all_songs = list_songs()
        assert len(all_songs) >= 3
        
        # Test filtering by genre
        genre_songs = list_songs(genre='Test Genre')
        assert len(genre_songs) >= 2
        assert all(song.genre == 'Test Genre' for song in genre_songs)
        
        # Test pagination
        paginated_songs = list_songs(limit=1, offset=1)
        assert len(paginated_songs) == 1
        
    finally:
        # Clean up
        for song in songs:
            delete_song(song.id)

def test_list_songs_empty(db_connection):
    """Test listing songs when no songs match the filter."""
    songs = list_songs(genre='Non-existent Genre')
    assert len(songs) == 0 