import json
import os
import boto3
from datetime import datetime
from typing import Dict, Any
from src.database.operations import (
    create_song,
    get_song,
    update_song,
    delete_song,
    list_songs,
    Song,
    DatabaseError,
    SongNotFoundError,
    InvalidDataError,
)

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function handler for the OurChants API.
    Handles all song-related operations through API Gateway.
    """
    try:
        # Get HTTP method and path
        http_method = event['httpMethod']
        path = event['path']
        
        # Handle different endpoints
        if path == '/songs':
            if http_method == 'GET':
                # List all songs
                limit = int(event.get('queryStringParameters', {}).get('limit', 10))
                offset = int(event.get('queryStringParameters', {}).get('offset', 0))
                genre = event.get('queryStringParameters', {}).get('genre')
                artist = event.get('queryStringParameters', {}).get('artist')
                
                songs = list_songs(limit=limit, offset=offset, genre=genre, artist=artist)
                return {
                    'statusCode': 200,
                    'body': json.dumps([song.__dict__ for song in songs])
                }
                
            elif http_method == 'POST':
                # Create new song
                body = json.loads(event['body'])
                song = create_song(body)
                return {
                    'statusCode': 201,
                    'body': json.dumps(song.__dict__)
                }
                
        elif path.startswith('/songs/'):
            song_id = path.split('/')[-1]
            
            if http_method == 'GET':
                # Get single song
                song = get_song(song_id)
                return {
                    'statusCode': 200,
                    'body': json.dumps(song.__dict__)
                }
                
            elif http_method == 'PUT':
                # Update song
                body = json.loads(event['body'])
                song = update_song(song_id, body)
                return {
                    'statusCode': 200,
                    'body': json.dumps(song.__dict__)
                }
                
            elif http_method == 'DELETE':
                # Delete song
                delete_song(song_id)
                return {
                    'statusCode': 204,
                    'body': ''
                }
                
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not Found'})
        }
        
    except SongNotFoundError as e:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': str(e)})
        }
    except InvalidDataError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except DatabaseError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        } 