import json
import os
from datetime import datetime
from models.song import Song

def test_json_file_exists():
    """Test that the JSON file exists and is accessible."""
    assert os.path.exists('data/sample_songs.json'), "JSON file not found"

def test_json_structure():
    """Test that the JSON file has the correct structure."""
    with open('data/sample_songs.json', 'r') as f:
        data = json.load(f)
        
    # Check top-level structure
    assert 'songs' in data, "Missing 'songs' key in JSON"
    assert isinstance(data['songs'], list), "'songs' should be a list"
    assert len(data['songs']) == 10, "Should have exactly 10 songs"
    
    # Check each song's structure
    required_fields = {'id', 'name', 'artist', 'album', 'release_date', 'genre', 'duration_in_seconds'}
    for song in data['songs']:
        assert all(field in song for field in required_fields), f"Missing required field in song {song['id']}"
        assert isinstance(song['duration_in_seconds'], int), f"Duration should be an integer in song {song['id']}"
        assert song['duration_in_seconds'] > 0, f"Duration should be positive in song {song['id']}"
        
        # Test date format
        try:
            datetime.strptime(song['release_date'], '%Y-%m-%d')
        except ValueError:
            assert False, f"Invalid date format in song {song['id']}"

def test_song_creation_from_json():
    """Test that songs can be created from JSON data."""
    with open('data/sample_songs.json', 'r') as f:
        data = json.load(f)
    
    for song_data in data['songs']:
        # Convert date string to datetime
        release_date = datetime.strptime(song_data['release_date'], '%Y-%m-%d')
        
        # Create Song instance
        song = Song(
            id=song_data['id'],
            name=song_data['name'],
            artist=song_data['artist'],
            album=song_data['album'],
            release_date=release_date,
            genre=song_data['genre'],
            duration_in_seconds=song_data['duration_in_seconds']
        )
        
        # Verify the song was created correctly
        assert song.id == song_data['id']
        assert song.name == song_data['name']
        assert song.artist == song_data['artist']
        assert song.album == song_data['album']
        assert song.genre == song_data['genre']
        assert song.duration_in_seconds == song_data['duration_in_seconds'] 