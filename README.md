# OurChants - Song Data Management

A Python application for managing song data with a robust data model and test suite.

## Project Structure

```
ourchants/
├── models/
│   ├── __init__.py
│   └── song.py
├── tests/
│   └── test_song.py
├── pyproject.toml
├── setup.py
└── README.md
```

## Features

- Data model for song information using Python dataclasses
- Built-in validation for song data
- Comprehensive test suite
- Type hints for better code maintainability

## Data Model

The `Song` class includes the following fields:
- `id`: Unique identifier for the song
- `name`: Song title
- `artist`: Artist name
- `album`: Album name
- `release_date`: Release date as a datetime object
- `genre`: Music genre
- `duration_in_seconds`: Song length in seconds
- `description`: Optional field for additional information

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip3 (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ourchants.git
cd ourchants
```

2. Install the package in development mode:
```bash
pip3 install -e .
```

3. Install the test dependencies:
```bash
pip3 install pytest
```

### Running Tests

To run the test suite:
```bash
python3 -m pytest tests/test_song.py
```

## Usage Example

```python
from datetime import datetime
from models.song import Song

# Create a new song
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

# Access song properties
print(f"Song: {song.name}")
print(f"Artist: {song.artist}")
print(f"Duration: {song.duration_in_seconds} seconds")
```

## Validation Rules

The data model includes the following validation rules:
- Duration must be a positive number
- Song name cannot be empty
- Artist name cannot be empty

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Cursor Prompt
The few-shot prompt that generated this code was:
```
Create a Python data model for an application where users can store and interact with song data. The model should include fields like id, name, artist, album, release_date, genre, and duration_in_seconds. The data model should be structured using Python classes, and make sure to use dataclasses for simplicity. Include a test that creates an instance of the data model and checks if it can be initialized properly with sample data.
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.