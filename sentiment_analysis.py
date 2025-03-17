from transformers import pipeline

# Load sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text):
    """
    Performs sentiment analysis on the given text.
    
    Args:
        text (str): The text to analyze.
    
    Returns:
        str: Sentiment label (Positive, Negative, or Neutral)
    """
    result = sentiment_pipeline(text[:512])  # Limit text length to 512 characters for efficiency
    sentiment = result[0]['label']
    
    return "Positive" if sentiment == "POSITIVE" else "Negative" if sentiment == "NEGATIVE" else "Neutral"
