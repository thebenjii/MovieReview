import tkinter as tk
from tkinter import scrolledtext, messagebox, font as tkfont
import pandas as pd
import re
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Assuming paths are correct; replace with your actual file paths
DATA_DIR = 'Data'  # Update with the actual path
MOVIES_FILE_PATH = DATA_DIR + '/movies.csv'
RATINGS_FILE_PATH = DATA_DIR + '/ratings.csv'
REVIEWS_FILE_PATH = DATA_DIR + '/IMDB Dataset.csv'

def load_data():
    try:
        logging.info("Loading data...")
        movies = pd.read_csv(MOVIES_FILE_PATH)
        ratings = pd.read_csv(RATINGS_FILE_PATH)
        reviews = pd.read_csv(REVIEWS_FILE_PATH)

        logging.info(f"Movies columns: {movies.columns.tolist()}")
        logging.info(f"Ratings columns: {ratings.columns.tolist()}")
        logging.info(f"Reviews columns: {reviews.columns.tolist()}")

        # Normalize movie titles for better matching
        movies['normalized_title'] = movies['title'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x).lower().strip())

        # Merge movies and ratings
        movie_ratings = pd.merge(movies, ratings, on='movieId', how='left')
        movie_ratings = movie_ratings.groupby('movieId').agg(
            average_rating=('rating', 'mean'),
            rating_count=('rating', 'count')
        ).reset_index()
        movies = pd.merge(movies, movie_ratings[['movieId', 'average_rating', 'rating_count']], on='movieId', how='left')

        return movies, reviews
    except Exception as e:
        logging.error("Failed to load data files: {}".format(e))
        return None, None

movies, reviews = load_data()

class MovieReviewerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Reviewer")
        self.configure(bg="#F0F0F0")  # Light grey background
        self.custom_font = tkfont.Font(family="Arial", size=12)
        self.setup_ui()

    def setup_ui(self):
        self.movie_entry = tk.Entry(self, width=50, font=self.custom_font, bg="#FFFFFF", fg="#333333")
        self.movie_entry.pack(pady=10)
        tk.Button(self, text="Search", command=self.search_and_display_movies, bg="#4CAF50", fg="#FFFFFF", font=self.custom_font).pack(pady=10)
        self.details_text = scrolledtext.ScrolledText(self, width=60, height=4, font=self.custom_font, bg="#FFFFFF", fg="#333333")
        self.details_text.pack(pady=10)
        self.details_text.config(state=tk.DISABLED)
        self.reviews_text = scrolledtext.ScrolledText(self, width=60, height=10, font=self.custom_font, bg="#FFFFFF", fg="#333333")
        self.reviews_text.pack(pady=10)
        self.reviews_text.config(state=tk.DISABLED)

    def search_and_display_movies(self):
        search_query = self.movie_entry.get()
        if not search_query:
            messagebox.showinfo("Input Required", "Please enter a movie name or keyword.")
            return
        search_query_normalized = re.sub(r'[^a-zA-Z0-9\s]', '', search_query).lower().strip()
        matched_movies = movies[movies['normalized_title'].str.contains(search_query_normalized, na=False)]
        if matched_movies.empty:
            messagebox.showinfo("No Results", "No movies found matching the query.")
            return
        self.display_movie_details(matched_movies.iloc[0]['movieId'])

    def display_movie_details(self, movie_id):
        movie_info = movies[movies['movieId'] == movie_id].iloc[0]
        details = f"Title: {movie_info['title']}\nGenres: {movie_info['genres']}\nAverage Rating: {movie_info['average_rating']:.2f} (from {movie_info['rating_count']} ratings)\n"
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete('1.0', tk.END)
        self.details_text.insert(tk.END, details)
        self.details_text.config(state=tk.DISABLED)
        relevant_reviews = reviews[reviews['review'].str.lower().str.contains(movie_info['title'].lower())]
        sample_reviews = relevant_reviews['review'].sample(min(5, len(relevant_reviews))).tolist() if not relevant_reviews.empty else ["No reviews available."]
        self.reviews_text.config(state=tk.NORMAL)
        self.reviews_text.delete('1.0', tk.END)
        self.reviews_text.insert(tk.END, "Sample Reviews:\n" + "\n".join(sample_reviews))
        self.reviews_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = MovieReviewerApp()
    app.mainloop()
