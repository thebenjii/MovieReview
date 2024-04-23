import pandas as pd
import logging
import re

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load data
def load_data():
    try:
        logging.info("Loading data...")
        movies = pd.read_csv('/full/path/to/Data/movies.csv')
        ratings = pd.read_csv('/full/path/to/Data/ratings.csv')
        reviews = pd.read_csv('/full/path/to/Data/IMDB Dataset.csv')

        logging.info(f"Movies columns: {movies.columns.tolist()}")
        logging.info(f"Ratings columns: {ratings.columns.tolist()}")
        logging.info(f"Reviews columns: {reviews.columns.tolist()}")

        # rest of your code...

    except Exception as e:
        logging.error(f"Failed to load data files: {e}")
        return None, None


movies, reviews = load_data()

def search_and_display_movies(search_query):
    if not search_query:
        logging.info("No search query provided.")
        return

    search_query_normalized = re.sub(r'[^a-zA-Z0-9\s]', '', search_query).lower().strip()
    matched_movies = movies[movies['normalized_title'].str.contains(search_query_normalized, na=False)]

    if matched_movies.empty:
        logging.info("No movies found matching the query.")
        return

    for index, movie in matched_movies.iterrows():
        movie_id = movie['movieId']
        display_movie_details(movie_id)

def display_movie_details(movie_id):
    movie_info = movies[movies['movieId'] == movie_id].iloc[0]
    details = f"Title: {movie_info['title']}\nGenres: {movie_info['genres']}\nAverage Rating: {movie_info['average_rating']:.2f} (from {movie_info['rating_count']} ratings)\n"
    print(details)

    # matching reviews based on title presence in review text
    reviews['normalized_review'] = reviews['review'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x).lower().strip())
    relevant_reviews = reviews[reviews['normalized_review'].str.contains(movie_info['normalized_title'], na=False)]
    sample_reviews = relevant_reviews['review'].sample(min(5, len(relevant_reviews))).tolist() if not relevant_reviews.empty else ["No reviews available."]
    print("Sample Reviews:")
    for review in sample_reviews:
        print(review)
    print("\n")

# read in user input and display movie details
search_query = input("Enter a movie title to search: ")
search_and_display_movies(search_query)
