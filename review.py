import csv

def analyze_movie_reviews(csv_filepath):
    print("Opening file:", csv_filepath)  # Debug print
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print("File opened successfully")  # Debug print

        movie_name = input("Enter the movie name or a keyword from the movie title: ")
        total_reviews = 0
        positive_reviews = 0

        # Define lists of positive and negative words
        positive_words = ['good', 'great', 'awesome', 'excellent', 'positive', 'enjoyable', 'happy', 'love', 'liked', 'wonderful']
        negative_words = ['bad', 'terrible', 'awful', 'worst', 'negative', 'hate', 'disliked', 'poor', 'disappointing', 'sad']

        for row in reader:
            if movie_name.lower() in row['review'].lower():
                total_reviews += 1
                # Basic sentiment analysis
                score = 0
                words = row['review'].split()
                for word in words:
                    if word.lower() in positive_words:
                        score += 1
                    elif word.lower() in negative_words:
                        score -= 1

                if score > 0:
                    positive_reviews += 1

        if total_reviews > 0:
            positive_percentage = (positive_reviews / total_reviews) * 100
            print(f"Number of reviews found: {total_reviews}")
            print(f"Percentage of positive reviews: {positive_percentage:.2f}%")
        else:
            print("No reviews found for this movie.")

# Specify the path to your CSV file
csv_path = 'IMDB Dataset.csv'  # Ensure this path is correct
analyze_movie_reviews(csv_path)
