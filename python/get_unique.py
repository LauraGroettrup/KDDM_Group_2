import csv
import pandas as pd

unique_genres = set()

with open('cleaned_file.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        genres = row[3].replace('"', '').split(',')
        for genre in genres:
            unique_genres.add(genre)

df = pd.read_csv('short_filtered_file.csv')
print(df['titleType'].unique())


print(unique_genres)