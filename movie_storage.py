import json
import os


DATA_FILE = "data.json"  # JSON file storing movie data


def get_movies():
    """ Returns a dictionary of dictionaries that contains the movies information in the JSON file.
    The function loads the information from the JSON file and returns the data. """
    if not os.path.exists(DATA_FILE):
        return {}  # Return empty dictionary if file doesn't exist
    
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}  # Return empty dictionary if JSON is corrupted


def save_movies(movies):
    """ Gets all movies as an argument and saves them to the JSON file. """
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(movies, file, indent=4)


def add_movie(title, year, rating):
    """ Loads the information from the JSON file, adds the movie, and saves it to the JSON file. """
    movies = get_movies()
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)


def delete_movie(title):
    """ Loads the information from the JSON file, deletes the movie, and saves it. """
    movies = get_movies()  
    if title in movies:
        del movies[title]  
        save_movies(movies)


def update_movie(title, rating):
    """ Loads the information from the JSON file, updates the movie,
    and saves it. """
    movies = get_movies()  
    if title in movies:
        movies[title]["rating"] = rating  
        save_movies(movies)

