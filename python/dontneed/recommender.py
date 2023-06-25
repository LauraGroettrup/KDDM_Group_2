import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import pickle
import time

# Read csv
df = pd.read_csv('short_filtered_file.csv')


# Pre-processing steps
df['startYear'] = df['startYear'].apply(lambda x: str(int(x)) if x == x // 1 else np.nan)
df = df.dropna(subset=['startYear'])
df['startYear'] = df['startYear'].astype(int)
df['numVotes'] = df['numVotes'].fillna(0)
df['averageRating'] = df['averageRating'].fillna(0)

# Creating the metadata soup
df['metadata'] = df[['primaryTitle', 'startYear', 'genres']].astype(str).agg(' '.join, axis=1)

start_time = time.time()

# Creating the TF-IDF matrix
print("Starting TF-IDF Vectorization...")
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['metadata'])
print("TF-IDF Vectorization completed in: %s seconds." % (time.time() - start_time))

start_time = time.time()

# Calculating the cosine similarity
print("Starting Cosine Similarity calculation...")
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
print("Cosine Similarity calculation completed in: %s seconds." % (time.time() - start_time))

# Function that takes in movie title as input and outputs most similar movies
def recommend_movies(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = df[df['primaryTitle'] == title].index[0]

    # Get all movies with same cosine similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies (skip the first as it will be the input movie itself)
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df.iloc[movie_indices]

# Testing the recommender function
# print(recommend_movies('Carmencita'))

# Save the model
with open('tfidf_matrix.pkl', 'wb') as f:
    pickle.dump(tfidf_matrix, f)

with open('cosine_sim.pkl', 'wb') as f:
    pickle.dump(cosine_sim, f)
