# OurChants Development Documentation

## Project Vision
OurChants is an ambitious project to create a Spotify-like platform dedicated to sacred chants from various cultural and spiritual traditions worldwide. The platform aims to preserve, share, and celebrate these ancient musical forms while making them accessible to modern audiences.

## Development Phases

### Phase 1: Data Model Design
- Created Python dataclass model for song data
- Implemented validation rules
- Set up testing infrastructure
- Established core data structure

### Phase 2: Infrastructure Setup
- AWS CDK configuration
- PostgreSQL database deployment
- Security group configuration
- Environment variable management

### Phase 3: Database Implementation (Current)
- Database schema creation
- Data loading scripts
- Comprehensive test suite
- Connection management

#### Current Technical Implementation

##### Database Schema
```sql
-- Create songs table with optimized indexes
CREATE TABLE IF NOT EXISTS songs (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    album VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    genre VARCHAR(50) NOT NULL,
    duration_in_seconds INTEGER NOT NULL CHECK (duration_in_seconds > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for common query patterns
CREATE INDEX idx_songs_artist ON songs(artist);
CREATE INDEX idx_songs_genre ON songs(genre);
CREATE INDEX idx_songs_release_date ON songs(release_date);
CREATE INDEX idx_songs_name ON songs(name);
CREATE INDEX idx_songs_album ON songs(album);
```

##### Database Operations Module
The `src/database/operations.py` module provides a comprehensive set of CRUD operations for managing song data:

###### Song Data Class
```python
@dataclass
class Song:
    id: str
    name: str
    artist: str
    album: str
    release_date: date
    genre: str
    duration_in_seconds: int
    created_at: datetime = None
    updated_at: datetime = None
```

###### Key Features
1. **Connection Management**
   - Secure credential handling
   - Environment-based configuration
   - Connection pooling
   - Error handling

2. **CRUD Operations**
   - `create_song()`: Create new songs with validation
   - `get_song()`: Retrieve songs by ID
   - `update_song()`: Update song information
   - `delete_song()`: Remove songs
   - `list_songs()`: List songs with filtering and pagination

3. **Data Validation**
   - Required field checking
   - Type validation
   - Duration validation
   - Data integrity checks

4. **Error Handling**
   - `DatabaseError`: Base exception
   - `SongNotFoundError`: For missing songs
   - `InvalidDataError`: For invalid input

###### Example Usage
```python
# Create a new song
song_data = {
    'id': 'song-1',
    'name': 'Sacred Chant',
    'artist': 'Traditional',
    'album': 'Ancient Melodies',
    'release_date': date(2023, 1, 1),
    'genre': 'Sacred',
    'duration_in_seconds': 180
}
song = create_song(song_data)

# Update a song
updated_song = update_song('song-1', {'name': 'Updated Name'})

# Get a song
song = get_song('song-1')

# List songs
songs = list_songs(genre='Sacred', limit=10)
```

##### Test Suite
The test suite (`tests/test_database_operations.py`) verifies:
- Basic CRUD operations
- Data type integrity
- Filtering capabilities
- Statistical calculations
- Connection management
- Error handling

Key test cases:
1. `test_create_song`: Verifies song creation with validation
2. `test_get_song`: Tests song retrieval and error handling
3. `test_update_song`: Tests update operations and validation
4. `test_delete_song`: Tests deletion and existence checking
5. `test_list_songs`: Tests filtering and pagination

### Phase 4: API Layer (Planned)
1. RESTful API implementation
2. Authentication and authorization
3. Rate limiting and caching
4. API documentation

### Phase 5: Frontend Development (Planned)
1. React-based user interface
2. Audio player implementation
3. Search and discovery features
4. User profiles and playlists

### Phase 6: Advanced Features (Planned)
1. Recommendation engine
2. Social features
3. Content moderation
4. Analytics and reporting

## Technical Architecture

### Data Layer
- PostgreSQL database
- Optimized schema design
- Comprehensive indexing
- Data validation rules
- Connection management
- Error handling

### Infrastructure
- AWS RDS for database
- AWS Secrets Manager for credentials
- Environment-based configuration
- Automated deployment

### Testing Strategy
- Unit tests for core functionality
- Integration tests for database operations
- Data validation tests
- Performance testing
- Error scenario testing

## Development Guidelines

### Code Quality Standards
1. Comprehensive documentation
2. Type hints and validation
3. Error handling
4. Resource management
5. Test coverage
6. Code organization

### Testing Requirements
1. Unit test coverage
2. Data validation
3. Connection management
4. Performance considerations
5. Error scenario testing

### Deployment Process
1. Environment setup
2. Database provisioning
3. Schema deployment
4. Data loading
5. Testing
6. Monitoring

## Project Significance

### Cultural Preservation
- Digitizing ancient traditions
- Making sacred music accessible
- Supporting traditional artists

### Spiritual Connection
- Facilitating meditation and prayer
- Connecting diverse traditions
- Promoting spiritual exploration

### Technical Innovation
- Modern platform for ancient art
- Scalable architecture
- Global accessibility

## Getting Started

### Prerequisites
- Python 3.8+
- AWS CLI configured
- PostgreSQL client
- pip3

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

### Development Workflow
1. Create feature branch
2. Implement changes
3. Run tests:
   ```bash
   python -m pytest tests/
   ```
4. Submit pull request

### Deployment
1. Bootstrap CDK:
   ```bash
   cdk bootstrap
   ```
2. Deploy stack:
   ```bash
   cdk deploy
   ```
3. Set up database:
   ```bash
   python scripts/setup_database.py
   ```
4. Load sample data:
   ```bash
   python scripts/load_sample_data.py
   ```

## Contributing
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details. 