import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Load the dataset
data = pd.read_csv("../short_filtered_file.csv")

# Create a TF-IDF matrix of item descriptions
tfidf = TfidfVectorizer(stop_words="english")
data["genres"] = data["genres"].fillna("")
tfidf_matrix = tfidf.fit_transform(data["genres"])

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Build a reverse mapping of indices and movie titles
indices = pd.Series(data.index, index=data["primaryTitle"]).drop_duplicates()

# Function to get recommendations based on movie title
def get_recommendations(title, cosine_sim=cosine_sim, indices=indices):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return data["primaryTitle"].iloc[movie_indices]

# Example usage
recommendations = get_recommendations("Carmencita")
print(recommendations)