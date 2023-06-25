import dask.dataframe as dd
from dask_ml.feature_extraction.text import HashingVectorizer
from dask_ml.metrics.pairwise import pairwise_distances
from dask.distributed import Client
import pandas as pd


def main():
    data = dd.read_csv('short_filtered_file.csv')

    client = Client()

    data['metadata'] = data[['primaryTitle', 'startYear', 'genres']].astype(str).apply(' '.join, axis=1)

    vectorizer = HashingVectorizer(stop_words="english")
    matrix = vectorizer.transform(data['metadata'])

    # Since HashingVectorizer's output is a Dask Array, we need to compute it to a Dask Bag
    bag = matrix.to_bag()
    # Compute the pairwise distances (cosine similarity)
    cosine_sim = 1 - pairwise_distances(bag.compute(), metric='cosine')

    indices = pd.Series(data.index.compute(), index=data["primaryTitle"].compute()).drop_duplicates()
    # Function to get recommendations based on movie title
    def get_recommendations(title, cosine_sim=cosine_sim, indices=indices):
        idx = indices[title]  # Get the index of the movie that matches the title
        sim_scores = list(enumerate(cosine_sim[idx]))  # Get similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # Sort scores based on similarity
        sim_scores = sim_scores[1:11]  # Get top 10 similar movies
        movie_indices = [i[0] for i in sim_scores]  # Get movie indices
        return data["primaryTitle"].iloc[movie_indices].compute()  # Return movie titles

    # Example usage
    recommendations = get_recommendations('The Sea')
    print(recommendations)

if __name__ == '__main__':
    main()