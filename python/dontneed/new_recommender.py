import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import pickle


df = pd.read_csv('../short_filtered_file.csv')

df['metadata'] = df[['primaryTitle', 'startYear', 'genres']].astype(str).apply(' '.join, axis=1)


count_vectorizer = CountVectorizer(max_features=5000,stop_words="english")
count_matrix = count_vectorizer.fit_transform(df['metadata'])

print(count_matrix.shape)

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
print(cosine_sim2.shape)

movies_df = df.reset_index()
indices = pd.Series(movies_df.index, index=movies_df['primaryTitle']).drop_duplicates()

print(indices.head())

def get_recommendations(title, cosine_sim=cosine_sim2):
    idx = indices[title]
    similarity_scores = list(enumerate(cosine_sim[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:11]
    # (a, b) where a is id of movie, b is similarity_scores

    movies_indices = [ind[0] for ind in similarity_scores]
    movies = movies_df["primaryTitle"].iloc[movies_indices]
    return movies


print("################ Content Based System #############")
print("Batman")
print(get_recommendations("Batman", cosine_sim2))
