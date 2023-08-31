import nltk  # type: ignore
from nltk.sentiment import SentimentIntensityAnalyzer  # type: ignore

nltk.download("vader_lexicon")  # Download the sentiment analysis lexicon

# Sample README content
readme_content = """
Welcome to this project!
This project aims to provide a simple solution for data analysis.
"""

# Initialize the SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Perform sentiment analysis on the README content
sentiment_scores = sia.polarity_scores(readme_content)

# Interpret sentiment scores
if sentiment_scores["compound"] >= 0.05:
    sentiment = "Positive"
elif sentiment_scores["compound"] <= -0.05:
    sentiment = "Negative"
else:
    sentiment = "Neutral"

print("Sentiment Scores:", sentiment_scores)
print("Overall Sentiment:", sentiment)
