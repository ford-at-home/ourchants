from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Song:
    id: str
    name: str
    artist: str
    album: str
    release_date: datetime
    genre: str
    duration_in_seconds: int
    description: Optional[str] = None

    def __post_init__(self):
        if self.duration_in_seconds <= 0:
            raise ValueError("Duration must be a positive number")
        
        if not self.name.strip():
            raise ValueError("Song name cannot be empty")
        
        if not self.artist.strip():
            raise ValueError("Artist name cannot be empty") 