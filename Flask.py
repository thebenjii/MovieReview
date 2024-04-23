from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

# Load data
def load_data():
    movies = pd.read_csv('Data/movies.csv')
    ratings = pd.read_csv('Data/ratings.csv')
    reviews = pd.read_csv('Data/IMDB Dataset.csv')
    
    # Normalize titles for better matching
    movies['normalized_title'] = movies['title'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x).lower().strip())

    # Merge movies and ratings
    movie_ratings = pd.merge(movies, ratings, on='movieId', how='left')
    movie_ratings = movie_ratings.groupby('movieId').agg(
        average_rating=('rating', 'mean'),
        rating_count=('rating', 'count')
    ).reset_index()
    movies = pd.merge(movies, movie_ratings[['movieId', 'average_rating', 'rating_count']], on='movieId', how='left')
    
    return movies, reviews

movies, reviews = load_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form.get('search', '')
        if search_query:
            normalized_query = re.sub(r'[^a-zA-Z0-9\s]', '', search_query).lower().strip()
            matched_movies = movies[movies['normalized_title'].str.contains(normalized_query, na=False)]
            if not matched_movies.empty:
                movie_id = matched_movies.iloc[0]['movieId']
                return render_movie_details(movie_id)
            else:
                return render_template('index.html', error="No movies found.")
        else:
            return render_template('index.html', error="Please enter a movie name.")
    return render_template('index.html')

def render_movie_details(movie_id):
    movie_info = movies[movies['movieId'] == movie_id].iloc[0]
    relevant_reviews = reviews[reviews['review'].str.lower().str.contains(movie_info['title'].lower())]
    sample_reviews = relevant_reviews['review'].sample(min(5, len(relevant_reviews))).tolist() if not relevant_reviews.empty else ["No reviews available."]
    return render_template('details.html', movie=movie_info, reviews=sample_reviews)

if __name__ == '__main__':
    app.run(debug=True)

