"""_summary_
"""

import nltk  # type: ignore
from nltk.sentiment import SentimentIntensityAnalyzer  # type: ignore

nltk.download("vader_lexicon")  # Download the sentiment analysis lexicon


def get_readme_sentiment(readme_content: str) -> dict:
    """_summary_

    :param readme_content: _description_
    :type readme_content: str
    :return: _description_
    :rtype: dict
    """
    # Initialize the SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer()

    # Perform sentiment analysis on the README content
    sentiment_scores = sia.polarity_scores(readme_content)

    # Interpret sentiment scores
    if sentiment_scores["compound"] >= .05:
        sentiment = "Positive"
    elif sentiment_scores["compound"] <= -.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # print("Sentiment Scores:", sentiment_scores)
    # print("Overall Sentiment:", sentiment)

    return {
        "Sentiment Scores": sentiment_scores,
        "Overall Sentiment": sentiment
    }


def main() -> None:
    # Sample README content
    readme_content = """
    Welcome to this project!
    This project aims to provide a simple solution for data analysis.
    """

    readme_sentiment = get_readme_sentiment(readme_content)
    print(readme_sentiment)


if __name__ == "__main__":
    main()
