import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Styling constants
BG_COLOR = "#333333"
TEXT_COLOR = "#FFFFFF"
BUTTON_COLOR = "#006699"
HOVER_COLOR = "#005577"
FONT = ("Arial", 12)

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
                display_pie_chart(positive_reviews, total_reviews)
                return f"Number of reviews found: {total_reviews}\nPercentage of positive reviews: {positive_percentage:.2f}%"
            else:
                return "No reviews found for this movie."
    except Exception as e:
        return str(e)

def display_pie_chart(positive, total):
    labels = 'Positive', 'Negative/Neutral'
    sizes = [positive, total - positive]
    colors = ['#ff9999','#66b3ff']
    explode = (0.1, 0)  

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')

    canvas = FigureCanvasTkAgg(fig1, master=result_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

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

def on_enter(e, btn):
    btn['background'] = HOVER_COLOR

def on_leave(e, btn):
    btn['background'] = BUTTON_COLOR

# Set up the main application window
root = tk.Tk()
root.title("Movie Review Sentiment Analysis")
root.configure(bg=BG_COLOR)

# Create widgets
file_label = tk.Label(root, text="No file loaded. Please load a CSV file.", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
file_label.pack(pady=10)

load_button = tk.Button(root, text="Load CSV File", command=load_file, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=FONT)
load_button.pack(pady=5)
load_button.bind("<Enter>", lambda e, btn=load_button: on_enter(e, btn))
load_button.bind("<Leave>", lambda e, btn=load_button: on_leave(e, btn))

movie_label = tk.Label(root, text="Enter Movie Name or Keyword:", bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
movie_label.pack(pady=10)

movie_entry = tk.Entry(root, width=50, font=FONT)
movie_entry.pack(pady=10)

analyze_button = tk.Button(root, text="Analyze", command=run_analysis, bg=BUTTON_COLOR, fg=TEXT_COLOR, font=FONT)
analyze_button.pack(pady=10)
analyze_button.bind("<Enter>", lambda e, btn=analyze_button: on_enter(e, btn))
analyze_button.bind("<Leave>", lambda e, btn=analyze_button: on_leave(e, btn))

result_text = scrolledtext.ScrolledText(root, width=60, height=10, font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
result_text.pack(pady=10)

result_frame = tk.Frame(root, bg=BG_COLOR)  # Frame to hold the matplotlib canvas
result_frame.pack(fill=tk.BOTH, expand=True)

# Start the GUI event loop
root.mainloop()
