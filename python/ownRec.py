import json
import random
from collections import Counter

class Movie:
    def __init__(self, tconst, primaryTitle, genres, averageRating, **kwargs):
        self.tconst = tconst
        self.primaryTitle = primaryTitle
        self.genres = genres.split(',')
        self.averageRating = averageRating

def load_movies(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return [Movie(**movie) for movie in data]

def generate_list(n):
    return [int(random.expovariate(0.05)) for _ in range(n)]

def calculate_genre_percentages(movies):
    genre_count = {}
    total_genres = 0

    for movie in movies:
        unique_genres = set(movie.genres)
        total_genres += len(unique_genres)

        for genre in unique_genres:
            if genre in genre_count:
                genre_count[genre] += 1
            else:
                genre_count[genre] = 1

    genre_percentages = []

    for genre, count in genre_count.items():
        percentage = round((count / total_genres), 3)
        genre_percentages.append((genre, percentage))

    return genre_percentages

def generate_movies(genre_percentages, num_movies):
    genres = [genre for genre, _ in genre_percentages]
    probabilities = [percentage for _, percentage in genre_percentages]

    movies = random.choices(genres, probabilities, k=num_movies)
    genre_counts = dict(Counter(movies))

    return genre_counts

def get_top_rated_movies_by_genre(movies, genre):
    genre_movies = [movie for movie in movies if genre in movie.genres]
    sorted_movies = sorted(genre_movies, key=lambda movie: movie.averageRating, reverse=True)
    top_rated_movies = [(movie.primaryTitle, movie.genres, movie.averageRating) for movie in sorted_movies[:100]]
    return top_rated_movies

def generate_movies_with_indexes(movie_list, indexes):
    movies_with_indexes = []
    for index in indexes:
        if index < len(movie_list):
            movies_with_indexes.append(movie_list[index])
    return movies_with_indexes

def process_genre_counts(genre_counts, movies):
    selected_movies = []
    for genre, count in genre_counts.items():
        top_movies_genre = get_top_rated_movies_by_genre(movies, genre)
        selected_indexes = generate_list(count)
        selected_movies += generate_movies_with_indexes(top_movies_genre, selected_indexes)
    return selected_movies

# Load the movies
allMovies = load_movies('Movies.json')

def generate_liked_movies(movies, n):
    return random.sample(movies, n)

# Generate 10 liked movies
liked_movies = generate_liked_movies(allMovies, 10)

# Print liked movies
for movie in liked_movies:
    print(f"Genres: {', '.join(movie.genres)}")


# Calculate genre percentages
genre_percentages = calculate_genre_percentages(liked_movies)
print(genre_percentages)
# Example usage:

num_movies = 10
movieCounts = generate_movies(genre_percentages, num_movies)
print(movieCounts)

for movie in process_genre_counts(movieCounts, allMovies):
    print(movie)
