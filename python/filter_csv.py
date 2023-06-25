import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('IMDB.csv')

# Drop rows with incomplete data in any column
df.dropna(subset=[ 'primaryTitle','titleType', 'startYear', 'genres', 'averageRating','numVotes'], inplace=True)

genre_list = ['Animation', 'Game-Show', 'War', 'Drama', 'Adult', 'Biography', 'Adventure', 'Musical', 'News', 'Romance',
              'Documentary', 'Horror', 'Fantasy', 'History', 'Mystery', 'Reality-TV', 'Crime', 'Family', 'Thriller',
              'Film-Noir', 'Sci-Fi', 'Western', 'Sport', 'Talk-Show', 'Music', 'Short', 'Action', 'Comedy']

titleType_list = ['short' 'movie' 'tvShort' 'tvSeries' 'tvMovie' 'tvEpisode' 'tvMiniSeries'
 'tvSpecial' 'video' 'videoGame']

# Drop rows without specified genres
df = df[df['genres'].apply(lambda x: any([k in x for k in genre_list]))]

# Drop rows with "averageRating" not between 0 and 10
df = df[df['averageRating'].between(0, 10)]

# Convert 'startYear' to numeric first, errors='coerce' will replace non numeric with NaN
df['startYear'] = pd.to_numeric(df['startYear'], errors='coerce')

# Now convert 'startYear' to integer
df['startYear'] = df['startYear'].apply(lambda x: int(x) if x == x // 1 else np.nan)

# Drop rows with NaN 'startYear'
df = df.dropna(subset=['startYear'])

# Keep only the rows with 'startYear' between 1700 and 2023
df = df[df['startYear'].between(1700, 2023)]

# Update "averageRating" to 0 if "numVotes" is 0
df.loc[df['numVotes'] == 0, 'averageRating'] = 0


# add imdb weighted rating
C = df['averageRating'].mean()
m = df['numVotes'].quantile(0.85)
def weighted_rating(x, m=m, C=C):
    v = x['numVotes']
    R = x['averageRating']
    return (v/(v+m) * R) + (m/(m+v) * C)

# create new column 'score' and calculate weighted ratings
df['score'] = df.apply(weighted_rating, axis=1)

# sort by score
f = df.sort_values(by='score',ascending=False)


## first all movie
df = df.sort_values(by=['titleType'], key=lambda x: x == 'movie', ascending=False)

# Save the cleaned dataframe
df.to_csv('short_filtered_file.csv', index=False)
print("Filtered!")


