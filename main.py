from data.storage_json import StorageJson
from movie_app import MovieApp


def main():
    """
    Main entry point of the movie application.
    Initializes the storage and movie app, then runs the application.
    """
    # Create a storage instance
    storage = StorageJson('data/movies.json')
    
    # Create and run the movie app
    app = MovieApp(storage)
    app.run()


if __name__ == '__main__':
    main() 