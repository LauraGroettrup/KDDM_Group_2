import joblib
def recommend_movies(movie_titles):
    model = joblib.load('../movie_recommender.pkl')
    df = joblib.load('../movies.pkl')
    vectorizer = joblib.load('../vectorizer.pkl')

    recommendations = set()
    keyword_recommendations = set()

    for movie_title in movie_titles:
        input_data = df[df['primaryTitle'] == movie_title]

        if len(input_data) == 0:
            print(f'Movie "{movie_title}" not found in database')
            continue

        distances, indices = model.kneighbors(vectorizer.transform(input_data['genres']), n_neighbors=21)

        for i in range(1, len(distances.flatten())):
            movie = df.iloc[indices.flatten()[i]]['primaryTitle']
            if any(keyword.lower() in movie.lower() for keyword in movie_title.split()):
                keyword_recommendations.add(movie)
            else:
                recommendations.add(movie)

    all_recommendations = list(keyword_recommendations) + list(recommendations)

    for i, movie in enumerate(all_recommendations[:10]):
        print(f'{i + 1}: {movie}')


recommend_movies(['Batman and Robin', 'Batman Returns', 'Batman Forever', 'The New Batman Adventures', 'Batman Beyond', 'Batman Beyond: Return of the Joker'])