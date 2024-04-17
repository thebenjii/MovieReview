import csv

def analyze_movie_reviews(csv_filepath):
    print("Opening file:", csv_filepath)  # Debug print
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print("File opened successfully")  # Debug print
        
        movie_name = input("Enter the movie name or a keyword from the movie title: ")
        total_reviews = 0
        positive_reviews = 0

        for row in reader:
            if movie_name.lower() in row['review'].lower():
                total_reviews += 1
                if row['sentiment'] == 'positive':
                    positive_reviews += 1

        if total_reviews > 0:
            positive_percentage = (positive_reviews / total_reviews) * 100
            print(f"Number of reviews found: {total_reviews}")
            print(f"Percentage of positive reviews: {positive_percentage:.2f}%")
        else:
            print("No reviews found for this movie.")

csv_path = 'IMDB Dataset.csv'  # Ensure this path is correct
analyze_movie_reviews(csv_path)
