import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Load the data
df = pd.read_csv('../short_filtered_file.csv')

# Fill NA values
df['genres'] = df['genres'].fillna('')

# Convert genres to lower case and replace commas with spaces
df['genres'] = df['genres'].apply(lambda x: ' '.join(x.lower() for x in x.split(',')))

# Combine genres and primaryTitle into a single string
df['features'] = df['primaryTitle'] + ' ' + df['genres']

# Extract features with TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['features'])

# Fit nearest neighbors model
model = NearestNeighbors(metric='cosine', algorithm='brute')
model.fit(X)

# Save the model and other objects
import joblib
joblib.dump(model, '../movie_recommender.pkl')
joblib.dump(df, '../movies.pkl')
joblib.dump(vectorizer, '../vectorizer.pkl')
