import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import pickle

class MovieRecommender:

    def __init__(self):
        self.df = None
        self.cosine_sim = None
        self.indices = None

    def load_and_process_data(self, filename):
        self.df = pd.read_csv(filename)

        # Combine all the relevant columns into a single column for the vectorizer
        self.df['metadata'] = self.df[['primaryTitle', 'startYear', 'genres']].astype(str).apply(' '.join, axis=1)

    def compute_similarity(self):
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(self.df['metadata'])
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Create a reverse map of movie titles and dataframe indices
        self.indices = pd.Series(self.df.index, index=self.df['primaryTitle']).drop_duplicates()

    def recommend_movies(self, title):
        idx = self.indices[title]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        movie_indices = [i[0] for i in sim_scores]
        recommended_df = self.df.iloc[movie_indices]

        # Recommend movies with higher ratings and more votes
        recommended_df['score'] = recommended_df['averageRating'] * np.log(recommended_df['numVotes'])
        recommended_df = recommended_df.sort_values('score', ascending=False)

        return recommended_df['primaryTitle']

    def save_model(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump((self.df, self.cosine_sim, self.indices), f)

    def load_model(self, filename):
        with open(filename, 'rb') as f:
            self.df, self.cosine_sim, self.indices = pickle.load(f)

if __name__ == "__main__":
    recommender = MovieRecommender()
    with ProcessPoolExecutor() as executor:
        executor.submit(recommender.load_and_process_data, 'filtered_file.csv')
        executor.submit(recommender.compute_similarity)

    recommender.save_model('recommender_model.pkl')
