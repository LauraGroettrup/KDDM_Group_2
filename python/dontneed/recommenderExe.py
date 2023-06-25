import pickle
import os
import numpy as np

class MovieRecommender:

    def __init__(self):
        self.df = None
        self.cosine_sim = None
        self.indices = None

    def load_model(self, filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Could not find file {filename}")

        with open(filename, 'rb') as f:
            try:
                self.df, self.cosine_sim, self.indices = pickle.load(f)
            except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError):
                raise ValueError(f"Error loading model from file {filename}. The file might be corrupted or the model was saved in a different structure.")

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

        return recommended_df['primaryTitle'].tolist()

    def recommend_movies_list(self, titles):
        recommendations = []
        for title in titles:
            try:
                recommended_movies = self.recommend_movies(title)
                recommendations.append(recommended_movies)
            except KeyError:
                print(f"Movie: {title} not in database.")
                recommendations.append([])
        return recommendations

if __name__ == "__main__":
    recommender = MovieRecommender()
    recommender.load_model('recommender_model.pkl')

    movie_list = ['Carmencita']  # Input your list of movies here
    recommendations = recommender.recommend_movies_list(movie_list)
    for i in range(len(movie_list)):
        print(f'Movie: {movie_list[i]}')
        print('Recommended Movies:')
        print(recommendations[i])


loaded_recommender = MovieRecommender()
loaded_recommender.load_model('recommender_model.pkl')
print(loaded_recommender.df.head())
print(loaded_recommender.cosine_sim)
print(loaded_recommender.indices)