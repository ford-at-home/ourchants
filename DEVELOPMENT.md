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

##### Test Suite
The test suite (`tests/test_database_queries.py`) verifies:
- Basic CRUD operations
- Data type integrity
- Filtering capabilities
- Statistical calculations
- Connection management

Key test cases:
1. `test_query_all_songs`: Verifies complete data structure
2. `test_query_by_genre`: Tests genre-based filtering
3. `test_query_by_artist`: Tests artist-based filtering
4. `test_query_song_duration`: Tests aggregate calculations

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

## Development Guidelines

### Code Quality Standards
1. Comprehensive documentation
2. Type hints and validation
3. Error handling
4. Resource management

### Testing Requirements
1. Unit test coverage
2. Data validation
3. Connection management
4. Performance considerations

### Deployment Process
1. Environment setup
2. Database provisioning
3. Schema deployment
4. Data loading

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