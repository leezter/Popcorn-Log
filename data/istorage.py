from abc import ABC, abstractmethod


class IStorage(ABC):
    """Interface for movie storage operations.
    
    This abstract class defines the contract that all storage implementations must follow.
    It provides the basic CRUD (Create, Read, Update, Delete) operations for managing
    movie data.
    """

    @abstractmethod
    def list_movies(self):
        """Retrieve all movies from the storage.
        
        Returns:
            dict: A dictionary of movies where the key is the movie title and the value
                 contains movie details (year, rating, poster).
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def delete_movie(self, title):
        """Delete a movie from the storage.
        
        Args:
            title (str): The title of the movie to delete.
        
        Returns:
            bool: True if the movie was deleted successfully, False otherwise.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """Update the rating of a movie in the storage.
        
        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating for the movie.
        
        Returns:
            bool: True if the movie was updated successfully, False otherwise.
        """
        pass 