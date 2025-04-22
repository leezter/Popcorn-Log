import json
from typing import Dict, Any
from data.istorage import IStorage


class StorageJson(IStorage):
    """A JSON file-based implementation of the movie storage interface."""
    
    def __init__(self, file_path):
        """Initialize the JSON storage with the given file path.
        
        Args:
            file_path (str): Path to the JSON file that stores the movies.
        """
        self._file_path = file_path
        try:
            with open(self._file_path, 'r') as file:
                self._movies = json.load(file)
        except FileNotFoundError:
            self._movies = {}
            self._save_movies()


    def list_movies(self):
        """Retrieve all movies from the storage.
        
        Returns:
            dict: A dictionary of movies where the key is the movie title and the value
                 contains movie details (year, rating, poster).
        """
        return self._movies
    

    def _save_movies(self):
        """Helper method to save movies to the JSON file."""
        with open(self._file_path, 'w') as file:
            json.dump(self._movies, file, indent=4)


    def add_movie(self, title, year, rating, poster):
        """Add a new movie to the storage.
        
        Args:
            title (str): The title of the movie.
            year (str): The release year of the movie.
            rating (float): The rating of the movie.
            poster (str): URL or path to the movie's poster image.
        
        Returns:
            bool: True if the movie was added successfully, False otherwise.
        """
        if title in self._movies:
            return False
        
        self._movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster
        }
        self._save_movies()
        return True


    def delete_movie(self, title):
        """Delete a movie from the storage.
        
        Args:
            title (str): The title of the movie to delete.
        
        Returns:
            bool: True if the movie was deleted successfully, False otherwise.
        """
        if title not in self._movies:
            return False
        
        del self._movies[title]
        self._save_movies()
        return True


    def update_movie(self, title, rating):
        """Update the rating of a movie in the storage.
        
        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating for the movie.
        
        Returns:
            bool: True if the movie was updated successfully, False otherwise.
        """
        if title not in self._movies:
            return False
        
        self._movies[title]["rating"] = rating
        self._save_movies()
        return True 