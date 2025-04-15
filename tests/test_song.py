from datetime import datetime
import pytest
from models.song import Song

def test_song_creation():
    # Create a sample song
    song = Song(
        id="123",
        name="Bohemian Rhapsody",
        artist="Queen",
        album="A Night at the Opera",
        release_date=datetime(1975, 10, 31),
        genre="Rock",
        duration_in_seconds=354,
        description="A classic rock masterpiece"
    )

    # Verify all fields are set correctly
    assert song.id == "123"
    assert song.name == "Bohemian Rhapsody"
    assert song.artist == "Queen"
    assert song.album == "A Night at the Opera"
    assert song.release_date == datetime(1975, 10, 31)
    assert song.genre == "Rock"
    assert song.duration_in_seconds == 354
    assert song.description == "A classic rock masterpiece"

def test_song_validation():
    # Test invalid duration
    with pytest.raises(ValueError, match="Duration must be a positive number"):
        Song(
            id="123",
            name="Test Song",
            artist="Test Artist",
            album="Test Album",
            release_date=datetime.now(),
            genre="Test",
            duration_in_seconds=-1
        )

    # Test empty name
    with pytest.raises(ValueError, match="Song name cannot be empty"):
        Song(
            id="123",
            name="",
            artist="Test Artist",
            album="Test Album",
            release_date=datetime.now(),
            genre="Test",
            duration_in_seconds=180
        )

    # Test empty artist
    with pytest.raises(ValueError, match="Artist name cannot be empty"):
        Song(
            id="123",
            name="Test Song",
            artist="",
            album="Test Album",
            release_date=datetime.now(),
            genre="Test",
            duration_in_seconds=180
        ) 