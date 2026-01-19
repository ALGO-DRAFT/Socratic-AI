from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text: str) -> dict:
    """
    Calculates the compound sentiment score.
    Returns a dictionary with score, label, and raw breakdown.
    """
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    # Thresholds based on VADER documentation
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
        
    return {
        "score": compound,
        "label": label,
        "details": scores
    }