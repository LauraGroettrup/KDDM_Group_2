import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib


def recommend_movies(movie_titles):
    model = joblib.load('../movie_recommender.pkl')
    df = joblib.load('../movies.pkl')
    vectorizer = joblib.load('../vectorizer.pkl')

    recommendations = set()

    for movie_title in movie_titles:
        input_data = df[df['primaryTitle'] == movie_title]

        if len(input_data) == 0:
            print(f'Movie "{movie_title}" not found in database')
            continue

        distances, indices = model.kneighbors(vectorizer.transform(input_data['genres']), n_neighbors=11)
        for i in range(1, len(distances.flatten())):
            movie = df.iloc[indices.flatten()[i]]['primaryTitle']
            recommendations.add(movie)

    for i, movie in enumerate(list(recommendations)[:10]):
        print(f'{i + 1}: {movie}')


recommend_movies(['Batman and Robin', 'Batman Returns', 'Batman Forever', 'The New Batman Adventures', 'Batman Beyond'])
