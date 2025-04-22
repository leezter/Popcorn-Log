import random
import requests
from typing import Callable, Dict, List, Tuple
from data.istorage import IStorage


class MovieApp:
    """Main application class for the movie database manager."""


    def __init__(self, storage: IStorage):
        """Initialize the movie application with a storage implementation.
        
        Args:
            storage (IStorage): An implementation of the IStorage interface
                              for movie data persistence.
        """
        self._storage = storage
        # OMDb API key
        self._api_key = "45ce7064"


    def _fetch_movie_data(self, title: str) -> Dict:
        """
        Fetch movie data from OMDb API.
        
        Args:
            title (str): Movie title to search for
            
        Returns:
            dict: Movie data from OMDb API or None if not found
        """
        # URL encode the title to handle spaces and special characters
        url = f"http://www.omdbapi.com/?apikey={self._api_key}&t={requests.utils.quote(title)}"
        try:
            response = requests.get(url)
            data = response.json()
            
            if data.get('Response') == 'True':
                # Extract IMDb rating and convert to float
                rating = 0.0
                if 'imdbRating' in data and data['imdbRating'] != 'N/A':
                    rating = float(data['imdbRating'])
                
                # Extract year and convert to integer
                year = 0
                if 'Year' in data and data['Year'] != 'N/A':
                    # Handle cases where year might be a range (e.g., "2020-2021")
                    year = int(data['Year'].split('–')[0])
                
                return {
                    'title': data['Title'],
                    'year': year,
                    'rating': rating,
                    'poster': data.get('Poster', '')
                }
            return None
        except (requests.RequestException, ValueError, KeyError) as e:
            print(f"Error fetching movie data: {e}")  # Add error logging
            return None


    def _command_list_movies(self):
        """List all movies in the database."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
            return
        
        print(f"\n{len(movies)} movies in total:")
        for title, data in movies.items():
            print(f"{title} ({data['year']}): {data['rating']}")


    def _command_add_movie(self) -> None:
        """Add a movie to the movie database."""
        title = input("Enter movie title: ")
        
        # Fetch movie data from OMDb API
        movie_data = self._fetch_movie_data(title)
        
        if movie_data:
            print("\nMovie found! Here's what we got:")
            print(f"Title: {movie_data['title']}")
            print(f"Year: {movie_data['year']}")
            print(f"Rating: {movie_data['rating']}")
            print(f"Poster URL: {movie_data['poster']}")
            
            confirm = input("\nDo you want to add this movie? (y/n): ").lower()
            if confirm == 'y':
                if self._storage.add_movie(
                    movie_data['title'],
                    movie_data['year'],
                    movie_data['rating'],
                    movie_data['poster']
                ):
                    print(f"\nMovie '{movie_data['title']}' successfully added")
                else:
                    print("\nError: Movie not added")
            else:
                print("\nMovie not added")
        else:
            print(f"\nError: Movie '{title}' not found in OMDb database")


    def _command_delete_movie(self):
        """Delete a movie from the database."""
        title = input("Enter movie title to delete: ")
        if self._storage.delete_movie(title):
            print(f"Movie '{title}' successfully deleted")
        else:
            print(f"Movie '{title}' not found")


    def _command_update_movie(self):
        """Update the rating of a movie in the database."""
        title = input("Enter movie title: ")
        rating = float(input("Enter new rating (0-10): "))
        
        if self._storage.update_movie(title, rating):
            print(f"Movie '{title}' successfully updated")
        else:
            print(f"Movie '{title}' not found")


    def _command_movie_stats(self):
        """Display statistics about the movies in the database."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
            return

        ratings = [movie['rating'] for movie in movies.values()]
        avg_rating = sum(ratings) / len(ratings)
        median_rating = sorted(ratings)[len(ratings) // 2]
        best_movie = max(movies.items(), key=lambda x: x[1]['rating'])
        worst_movie = min(movies.items(), key=lambda x: x[1]['rating'])

        print("\nMovie Statistics:")
        print(f"Average rating: {avg_rating:.2f}")
        print(f"Median rating: {median_rating:.2f}")
        print(f"Best movie: {best_movie[0]} ({best_movie[1]['rating']})")
        print(f"Worst movie: {worst_movie[0]} ({worst_movie[1]['rating']})")


    def _command_random_movie(self):
        """Select and display a random movie from the database."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
            return

        title = random.choice(list(movies.keys()))
        movie = movies[title]
        print(f"\nYour random movie is: {title}")
        print(f"Year: {movie['year']}")
        print(f"Rating: {movie['rating']}")


    def _command_search_movie(self):
        """Search for a movie by title."""
        search_term = input("Enter part of movie name: ").lower()
        movies = self._storage.list_movies()
        found = False

        for title, data in movies.items():
            if search_term in title.lower():
                print(f"{title} ({data['year']}): {data['rating']}")
                found = True

        if not found:
            print(f"No movies found containing '{search_term}'")


    def _command_movies_sorted(self):
        """Display all movies sorted by rating in descending order."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies found.")
            return

        sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
        print("\nMovies sorted by rating:")
        for title, data in sorted_movies:
            print(f"{title} ({data['year']}): {data['rating']}")


    def _generate_website(self):
        """Generate an HTML website displaying all movies."""
        movies = self._storage.list_movies()
        
        if not movies:
            print("No movies to display.")
            return
            
        html_content = """<html>
<head>
    <title>My Movie App</title>
    <link rel="stylesheet" href="style.css"/>
</head>
<body>
<div class="list-movies-title">
    <h1>Popcorn Log</h1>
</div>
<div>
    <ol class="movie-grid">
"""
        # Add each movie to the HTML
        for title, movie in movies.items():
            movie_html = f"""
        <li>
            <div class="movie">
                <img class="movie-poster"
                     src="{movie.get('poster', '')}"
                     title="{title}"/>
                <div class="movie-title">{title}</div>
                <div class="movie-year">{movie.get('year', '')}</div>
            </div>
        </li>
"""
            html_content += movie_html
            
        # Close the HTML tags
        html_content += """
    </ol>
</div>
</body>
</html>
"""
        
        # Write the HTML file
        try:
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("\nWebsite was generated successfully.")
            print("You can find it in 'index.html'")
        except Exception as e:
            print(f"\nError generating website: {e}")


    def run(self):
        """Run the movie application's main loop."""
        commands = {
            "1": ("List movies", self._command_list_movies),
            "2": ("Add movie", self._command_add_movie),
            "3": ("Delete movie", self._command_delete_movie),
            "4": ("Update movie", self._command_update_movie),
            "5": ("Movie statistics", self._command_movie_stats),
            "6": ("Random movie", self._command_random_movie),
            "7": ("Search movie", self._command_search_movie),
            "8": ("Movies sorted by rating", self._command_movies_sorted),
            "9": ("Generate website", self._generate_website),
            "0": ("Exit", None)
        }

        while True:
            print("\nMenu:")
            for key, (description, _) in commands.items():
                print(f"{key}. {description}")

            choice = input("\nEnter choice (0-9): ")
            if choice not in commands:
                print("Invalid choice! Please try again.")
                continue

            if choice == "0":
                print("Goodbye!")
                break

            commands[choice][1]() 