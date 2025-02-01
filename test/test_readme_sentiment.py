
from unittest.mock import patch, MagicMock
from src.readme_sentiment import get_readme_sentiment  # type: ignore

# Mock data for testing
MOCK_README_CONTENT = "This is a great project with amazing features!"

# Mock sentiment scores for different scenarios
MOCK_POSITIVE_SENTIMENT_SCORES = {
    "neg": 0.0,
    "neu": 0.5,
    "pos": 0.5,
    "compound": 0.8  # Positive sentiment
}

MOCK_NEGATIVE_SENTIMENT_SCORES = {
    "neg": 0.7,
    "neu": 0.2,
    "pos": 0.1,
    "compound": -0.6  # Negative sentiment
}

MOCK_NEUTRAL_SENTIMENT_SCORES = {
    "neg": 0.1,
    "neu": 0.8,
    "pos": 0.1,
    "compound": 0.0  # Neutral sentiment
}


@patch("src.readme_sentiment.SentimentIntensityAnalyzer")
def test_get_readme_sentiment_positive(mock_sia):
    # Mock the polarity_scores method
    mock_sia_instance = MagicMock()
    mock_sia_instance.polarity_scores.return_value = MOCK_POSITIVE_SENTIMENT_SCORES
    mock_sia.return_value = mock_sia_instance

    # Call the function
    result = get_readme_sentiment(MOCK_README_CONTENT)

    # Assertions
    assert result == {
        "Sentiment Scores": MOCK_POSITIVE_SENTIMENT_SCORES,
        "Overall Sentiment": "Positive"
    }
    mock_sia_instance.polarity_scores.assert_called_once_with(MOCK_README_CONTENT)


@patch("src.readme_sentiment.SentimentIntensityAnalyzer")
def test_get_readme_sentiment_negative(mock_sia):
    # Mock the polarity_scores method
    mock_sia_instance = MagicMock()
    mock_sia_instance.polarity_scores.return_value = MOCK_NEGATIVE_SENTIMENT_SCORES
    mock_sia.return_value = mock_sia_instance

    # Call the function
    result = get_readme_sentiment(MOCK_README_CONTENT)

    # Assertions
    assert result == {
        "Sentiment Scores": MOCK_NEGATIVE_SENTIMENT_SCORES,
        "Overall Sentiment": "Negative"
    }
    mock_sia_instance.polarity_scores.assert_called_once_with(MOCK_README_CONTENT)


@patch("src.readme_sentiment.SentimentIntensityAnalyzer")
def test_get_readme_sentiment_neutral(mock_sia):
    # Mock the polarity_scores method
    mock_sia_instance = MagicMock()
    mock_sia_instance.polarity_scores.return_value = MOCK_NEUTRAL_SENTIMENT_SCORES
    mock_sia.return_value = mock_sia_instance

    # Call the function
    result = get_readme_sentiment(MOCK_README_CONTENT)

    # Assertions
    assert result == {
        "Sentiment Scores": MOCK_NEUTRAL_SENTIMENT_SCORES,
        "Overall Sentiment": "Neutral"
    }
    mock_sia_instance.polarity_scores.assert_called_once_with(MOCK_README_CONTENT)
