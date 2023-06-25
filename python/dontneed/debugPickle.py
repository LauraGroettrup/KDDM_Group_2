import pickle

with open('../recommender_model.pkl', 'rb') as f:
    df, cosine_sim, indices = pickle.load(f)

print(df.head())
print(cosine_sim)
print(indices)