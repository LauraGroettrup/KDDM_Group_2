import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Load the data
df = pd.read_csv('short_filtered_file.csv')

# Fill NA values
df['genres'] = df['genres'].fillna('')

# Extract features with TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
df['genres'] = df['genres'].apply(lambda x: ' '.join(x.lower() for x in x.split(',')))
X = vectorizer.fit_transform(df['genres'])

# Fit nearest neighbors model
model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(X)

# Save the model
import joblib
joblib.dump(model, 'movie_recommender.pkl')
joblib.dump(df, 'movies.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
