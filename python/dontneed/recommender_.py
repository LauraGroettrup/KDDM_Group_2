import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load the dataset
data = pd.read_csv("../short_filtered_file.csv")


tfidf = TfidfVectorizer(stop_words="english")
data['genres'] = data['genres'].fillna('')
tfidf_matrix = tfidf.fit_transform(data['genres'])

# Compute the cosine similarity matrix for genres
cosine_sim_genres = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Normalize the numerical data
scaler = MinMaxScaler()
numerical_data = data[['averageRating', 'numVotes']].fillna(0)
numerical_data = scaler.fit_transform(numerical_data)

# Compute the cosine similarity matrix for numerical data
cosine_sim_numerical = cosine_similarity(numerical_data, numerical_data)

# Combine the two similarity matrices
cosine_sim = cosine_sim_genres * 0.5 + cosine_sim_numerical * 0.5

# Build a reverse mapping of indices and movie titles
indices = pd.Series(data.index, index=data["primaryTitle"]).drop_duplicates()

# Function to get recommendations based on movie title
def get_recommendations(title, cosine_sim=cosine_sim, indices=indices):
    idx = indices[title]  # Get the index of the movie that matches the title
    sim_scores = list(enumerate(cosine_sim[idx]))  # Get similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # Sort scores based on similarity
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]  # Get movie indices
    return data["primaryTitle"].iloc[movie_indices]  # Return movie titles

# Example usage
recommendations = get_recommendations("Batman")
print(recommendations)