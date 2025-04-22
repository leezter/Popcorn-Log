import csv
from typing import Dict, List, Any, Union
from data.istorage import IStorage

class StorageCsv(IStorage):
    # Define the columns as a class constant to ensure consistency
    COLUMNS = ['title', 'year', 'rating', 'poster', 'notes']

    def __init__(self, file_path: str):
        """
        Initialize the CSV storage with the given file path.
        
        Args:
            file_path (str): Path to the CSV file
        """
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """
        Ensure the CSV file exists with proper headers.
        If the file doesn't exist, create it with headers.
        """
        try:
            with open(self.file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                # Verify headers match expected columns
                if reader.fieldnames != self.COLUMNS:
                    # If headers don't match, rewrite the file with correct headers
                    self._write_all_movies({})
        except FileNotFoundError:
            # Create file with headers if it doesn't exist
            self._write_all_movies({})

    def list_movies(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns a dictionary of dictionaries that contains the movies information in the database.
        
        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of movies
        """
        movies = {}
        try:
            with open(self.file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convert year and rating to proper types
                    if row['year']:  # Check if year exists and is not empty
                        row['year'] = int(row['year'])
                    if row['rating']:  # Check if rating exists and is not empty
                        row['rating'] = float(row['rating'])
                    movies[row['title']] = row
        except FileNotFoundError:
            pass
        return movies

    def add_movie(self, title: str, year: int, rating: float, poster: str = "") -> bool:
        """
        Adds a movie to the movies database.
        
        Args:
            title (str): Title of the movie
            year (int): Year of the movie
            rating (float): Rating of the movie
            poster (str): URL of the movie poster
        """
        movies = self.list_movies()
        if title in movies:
            return False
        movies[title] = {
            'title': title,
            'year': year,
            'rating': rating,
            'poster': poster,
            'notes': ''
        }
        self._write_all_movies(movies)
        return True

    def delete_movie(self, title: str) -> bool:
        """
        Deletes a movie from the movies database.
        
        Args:
            title (str): Title of the movie to delete
        """
        movies = self.list_movies()
        if title not in movies:
            return False
        del movies[title]
        self._write_all_movies(movies)
        return True

    def update_movie(self, title: str, rating: float) -> bool:
        """
        Updates a movie's rating in the movies database.
        
        Args:
            title (str): Title of the movie to update
            rating (float): New rating for the movie
            
        Returns:
            bool: True if movie was updated successfully, False otherwise
        """
        movies = self.list_movies()
        if title not in movies:
            return False
        movies[title]['rating'] = float(rating)
        self._write_all_movies(movies)
        return True

    def _write_all_movies(self, movies: Dict[str, Dict[str, Any]]) -> None:
        """
        Helper method to write all movies to the CSV file.
        
        Args:
            movies (Dict[str, Dict[str, Any]]): Dictionary of movies to write
        """
        with open(self.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.COLUMNS)
            writer.writeheader()
            for movie in movies.values():
                writer.writerow({
                    'title': movie.get('title', ''),
                    'year': movie.get('year', ''),
                    'rating': movie.get('rating', ''),
                    'poster': movie.get('poster', ''),
                    'notes': movie.get('notes', '')
                }) 