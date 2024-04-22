import tkinter as tk
from tkinter import scrolledtext, messagebox, font as tkfont
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Styling constants
BG_COLOR = "#333333"
TEXT_COLOR = "#FFFFFF"
BUTTON_COLOR = "#006699"
HOVER_COLOR = "#005577"
FONT = ("Arial", 12)

# Assuming paths are correct; replace with your actual file paths
MOVIES_FILE_PATH = 'movies.csv'
RATINGS_FILE_PATH = 'ratings.csv'

# Load data
def load_data():
    movies = pd.read_csv(MOVIES_FILE_PATH)
    ratings = pd.read_csv(RATINGS_FILE_PATH)
    return pd.merge(movies, ratings, on='movie_id')

# Preload the data at startup
merged_data = load_data()

def analyze_movie_reviews(data, movie_name):
    try:
        filtered_data = data[data['movie_name'].str.contains(movie_name, case=False)]
        total_reviews = len(filtered_data)
        positive_reviews = filtered_data[filtered_data['sentiment'] == 'positive'].shape[0]

        if total_reviews > 0:
            positive_percentage = (positive_reviews / total_reviews) * 100
            display_pie_chart(positive_reviews, total_reviews)
            sample_reviews = filtered_data['review'].sample(min(5, total_reviews)).tolist()
            result = f"Number of reviews found: {total_reviews}\nPercentage of positive reviews: {positive_percentage:.2f}%"
            return result, sample_reviews
        else:
            return "No reviews found for this movie.", []
    except Exception as e:
        return f"An error occurred: {str(e)}", []

def display_pie_chart(positive, total):
    labels = 'Positive', 'Negative/Neutral'
    sizes = [positive, total - positive]
    colors = ['#ff9999','#66b3ff']
    explode = (0.1, 0)

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=result_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def run_analysis():
    movie_name = movie_entry.get()
    if not movie_name:
        messagebox.showinfo("Input Required", "Please enter a movie name or keyword.")
        return

    result, sample_reviews = analyze_movie_reviews(merged_data, movie_name)
    formatted_reviews = "\n".join(f"{i+1}. {review}" for i, review in enumerate(sample_reviews))
    result_text.config(state=tk.NORMAL)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, result + "\n\nSample Reviews:\n" + formatted_reviews)
    result_text.config(state=tk.DISABLED)

# Main application setup
root = tk.Tk()
root.title("Movie Review Sentiment Analysis")
root.configure(bg=BG_COLOR)

custom_font = tkfont.Font(family="Arial", size=12)

movie_label = tk.Label(root, text="Enter Movie Name or Keyword:", bg=BG_COLOR, fg=TEXT_COLOR, font=custom_font)
movie_label.pack(pady=10)

movie_entry = tk.Entry(root, width=50, font=custom_font)
movie_entry.pack(pady=10)

analyze_button = tk.Button(root, text="Analyze", command=run_analysis, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=custom_font)
analyze_button.pack(pady=10)

result_text = scrolledtext.ScrolledText(root, width=60, height=15, font=custom_font, bg=BG_COLOR, fg=TEXT_COLOR)
result_text.pack(pady=10)

result_frame = tk.Frame(root, bg=BG_COLOR)
result_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
