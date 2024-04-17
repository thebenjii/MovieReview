import csv
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog

def analyze_movie_reviews(csv_filepath, movie_name):
    try:
        with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            total_reviews = 0
            positive_reviews = 0

            for row in reader:
                if movie_name.lower() in row['review'].lower():
                    total_reviews += 1
                    if row['sentiment'] == 'positive':
                        positive_reviews += 1

            if total_reviews > 0:
                positive_percentage = (positive_reviews / total_reviews) * 100
                result = f"Number of reviews found: {total_reviews}\nPercentage of positive reviews: {positive_percentage:.2f}%"
            else:
                result = "No reviews found for this movie."
            return result
    except Exception as e:
        return str(e)

def run_analysis():
    movie_name = movie_entry.get()
    if not movie_name:
        messagebox.showinfo("Input Required", "Please enter a movie name or keyword.")
        return

    result = analyze_movie_reviews(csv_path, movie_name)
    result_text.config(state=tk.NORMAL)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, result)
    result_text.config(state=tk.DISABLED)

def load_file():
    global csv_path
    filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if filepath:
        csv_path = filepath
        file_label.config(text=f"Loaded: {filepath}")

# Set up the main application window
root = tk.Tk()
root.title("Movie Review Sentiment Analysis")

# Create widgets
file_label = tk.Label(root, text="No file loaded. Please load a CSV file.")
file_label.pack(pady=10)

load_button = tk.Button(root, text="Load CSV File", command=load_file)
load_button.pack(pady=5)

movie_label = tk.Label(root, text="Enter Movie Name or Keyword:")
movie_label.pack(pady=10)

movie_entry = tk.Entry(root, width=50)
movie_entry.pack(pady=10)

analyze_button = tk.Button(root, text="Analyze", command=run_analysis)
analyze_button.pack(pady=10)

result_text = scrolledtext.ScrolledText(root, width=60, height=10, state=tk.DISABLED)
result_text.pack(pady=10)

# Start the GUI event loop
root.mainloop()
