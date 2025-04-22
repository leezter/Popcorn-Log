# Popcorn Log

A Python application for managing your movie collection. Keep track of your movies, their ratings, and more with both JSON and CSV storage support.

## Features

- Add movies with title, year, rating, and poster information
- Delete movies from your collection
- Update movie ratings
- List all movies in your collection
- Fetch movie information automatically from OMDB API
- Multiple storage options:
  - JSON storage
  - CSV storage
- Generate statistics about your movie collection
- Search for movies in your collection
- Sort movies by different criteria

## Installation

1. Clone the repository:
```bash
git clone https://github.com/leezter/Popcorn-Log.git
cd Popcorn-Log
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

The application will start and present you with a menu of options to manage your movie collection.

## Storage Options

The application supports two storage backends:

1. JSON Storage (`data/storage_json.py`):
   - Stores movies in a JSON file
   - Default storage option
   - Easy to read and modify manually

2. CSV Storage (`data/storage_csv.py`):
   - Stores movies in a CSV file
   - Alternative storage option
   - Compatible with spreadsheet applications

## Project Structure

- `main.py` - Application entry point
- `movie_app.py` - Main application logic
- `data/`
  - `istorage.py` - Storage interface definition
  - `storage_json.py` - JSON storage implementation
  - `storage_csv.py` - CSV storage implementation
  - `movies.json` - Default JSON storage file
  - `movies.csv` - Default CSV storage file

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or bug fixes.

## License

This project is open source and available under the MIT License. 