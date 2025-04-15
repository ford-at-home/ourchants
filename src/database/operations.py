#!/usr/bin/env python3
"""
Database operations module for OurChants application.
Provides CRUD operations for song data in PostgreSQL database.
"""

import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
from datetime import datetime, date
from typing import Dict, List, Optional, Union
from dataclasses import dataclass

@dataclass
class Song:
    """Data class representing a song in the database."""
    id: str
    name: str
    artist: str
    album: str
    release_date: date
    genre: str
    duration_in_seconds: int
    created_at: datetime = None
    updated_at: datetime = None

    @classmethod
    def from_db_row(cls, row):
        """Create a Song instance from a database row."""
        # Convert the row to a dictionary if it's not already
        if not isinstance(row, dict):
            row = dict(row)
        
        # Extract only the fields we need
        song_data = {
            'id': row['id'],
            'name': row['name'],
            'artist': row['artist'],
            'album': row['album'],
            'release_date': row['release_date'],
            'genre': row['genre'],
            'duration_in_seconds': row['duration_in_seconds'],
            'created_at': row.get('created_at'),
            'updated_at': row.get('updated_at')
        }
        
        return cls(**song_data)

class DatabaseError(Exception):
    """Base exception for database operations."""
    pass

class SongNotFoundError(DatabaseError):
    """Raised when a song is not found in the database."""
    pass

class InvalidDataError(DatabaseError):
    """Raised when invalid data is provided for a song."""
    pass

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    try:
        # Get database credentials from environment variables
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_port = os.getenv('DB_PORT')

        # Verify all required environment variables are set
        if not all([db_host, db_name, db_user, db_password, db_port]):
            missing = []
            if not db_host: missing.append('DB_HOST')
            if not db_name: missing.append('DB_NAME')
            if not db_user: missing.append('DB_USER')
            if not db_password: missing.append('DB_PASSWORD')
            if not db_port: missing.append('DB_PORT')
            raise DatabaseError(f"Missing required environment variables: {', '.join(missing)}")

        # Connect to the database
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,  # Use the database name from environment
            user=db_user,
            password=db_password,
            port=db_port
        )
        return conn
    except psycopg2.OperationalError as e:
        raise DatabaseError(f"Failed to connect to database '{db_name}': {str(e)}")
    except Exception as e:
        raise DatabaseError(f"Database connection error: {str(e)}")

def create_song(song_data: Dict[str, Union[str, int, datetime.date]]) -> Song:
    """
    Create a new song in the database.
    
    Args:
        song_data: Dictionary containing song information
        
    Returns:
        Song object representing the created song
        
    Raises:
        InvalidDataError: If required fields are missing or invalid
        DatabaseError: If database operation fails
    """
    required_fields = ['id', 'name', 'artist', 'album', 'release_date', 'genre', 'duration_in_seconds']
    
    # Validate required fields
    missing_fields = [field for field in required_fields if field not in song_data]
    if missing_fields:
        raise InvalidDataError(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Validate duration
    if not isinstance(song_data['duration_in_seconds'], int) or song_data['duration_in_seconds'] <= 0:
        raise InvalidDataError("Duration must be a positive integer")
    
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                query = sql.SQL("""
                    INSERT INTO songs (id, name, artist, album, release_date, genre, duration_in_seconds)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING *
                """)
                cur.execute(query, (
                    song_data['id'],
                    song_data['name'],
                    song_data['artist'],
                    song_data['album'],
                    song_data['release_date'],
                    song_data['genre'],
                    song_data['duration_in_seconds']
                ))
                result = cur.fetchone()
                return Song.from_db_row(result)
    except psycopg2.IntegrityError as e:
        raise InvalidDataError(f"Invalid data provided: {str(e)}")
    except Exception as e:
        raise DatabaseError(f"Failed to create song: {str(e)}")

def get_song(song_id: str) -> Song:
    """
    Retrieve a song by its ID.
    
    Args:
        song_id: Unique identifier of the song
        
    Returns:
        Song object if found
        
    Raises:
        SongNotFoundError: If song with given ID doesn't exist
        DatabaseError: If database operation fails
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                query = sql.SQL("SELECT * FROM songs WHERE id = %s")
                cur.execute(query, (song_id,))
                result = cur.fetchone()
                
                if not result:
                    raise SongNotFoundError(f"Song with ID {song_id} not found")
                
                return Song.from_db_row(result)
    except SongNotFoundError:
        raise
    except Exception as e:
        raise DatabaseError(f"Failed to retrieve song: {str(e)}")

def update_song(song_id: str, update_data: Dict[str, Union[str, int, datetime.date]]) -> Song:
    """
    Update a song's information.
    
    Args:
        song_id: Unique identifier of the song to update
        update_data: Dictionary containing fields to update
        
    Returns:
        Updated Song object
        
    Raises:
        SongNotFoundError: If song with given ID doesn't exist
        InvalidDataError: If update data is invalid
        DatabaseError: If database operation fails
    """
    # Validate update data
    if not update_data:
        raise InvalidDataError("No update data provided")
    
    if 'duration_in_seconds' in update_data and (
        not isinstance(update_data['duration_in_seconds'], int) or 
        update_data['duration_in_seconds'] <= 0
    ):
        raise InvalidDataError("Duration must be a positive integer")
    
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                # Build dynamic update query
                set_clauses = []
                values = []
                for key, value in update_data.items():
                    set_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(key)))
                    values.append(value)
                
                query = sql.SQL("""
                    UPDATE songs
                    SET {}
                    WHERE id = %s
                    RETURNING *
                """).format(sql.SQL(', ').join(set_clauses))
                
                values.append(song_id)
                cur.execute(query, values)
                result = cur.fetchone()
                
                if not result:
                    raise SongNotFoundError(f"Song with ID {song_id} not found")
                
                return Song.from_db_row(result)
    except SongNotFoundError:
        raise  # Re-raise SongNotFoundError without wrapping
    except psycopg2.IntegrityError as e:
        raise InvalidDataError(f"Invalid update data: {str(e)}")
    except Exception as e:
        raise DatabaseError(f"Failed to update song: {str(e)}")

def delete_song(song_id: str) -> bool:
    """
    Delete a song from the database.
    
    Args:
        song_id: Unique identifier of the song to delete
        
    Returns:
        True if song was deleted, False if song didn't exist
        
    Raises:
        DatabaseError: If database operation fails
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("DELETE FROM songs WHERE id = %s RETURNING id")
                cur.execute(query, (song_id,))
                result = cur.fetchone()
                return bool(result)
    except Exception as e:
        raise DatabaseError(f"Failed to delete song: {str(e)}")

def list_songs(
    limit: int = 100,
    offset: int = 0,
    genre: Optional[str] = None,
    artist: Optional[str] = None
) -> List[Song]:
    """
    List songs with optional filtering.
    
    Args:
        limit: Maximum number of songs to return
        offset: Number of songs to skip
        genre: Filter by genre
        artist: Filter by artist
        
    Returns:
        List of Song objects
        
    Raises:
        DatabaseError: If database operation fails
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                query = sql.SQL("SELECT * FROM songs")
                conditions = []
                params = []
                
                if genre:
                    conditions.append(sql.SQL("genre = %s"))
                    params.append(genre)
                
                if artist:
                    conditions.append(sql.SQL("artist = %s"))
                    params.append(artist)
                
                if conditions:
                    query = sql.SQL("{} WHERE {}").format(
                        query,
                        sql.SQL(" AND ").join(conditions)
                    )
                
                query = sql.SQL("{} ORDER BY name LIMIT %s OFFSET %s").format(query)
                params.extend([limit, offset])
                
                cur.execute(query, params)
                results = cur.fetchall()
                return [Song.from_db_row(result) for result in results]
    except Exception as e:
        raise DatabaseError(f"Failed to list songs: {str(e)}") 