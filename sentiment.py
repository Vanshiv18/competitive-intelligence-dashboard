"""
Module 3: Sentiment & Positioning Engine
Maps to JD bullet: "competitors product positioning"

Reuses the kind of NLP pipeline from the E-Commerce Sentiment Analytics project.
Uses TextBlob for a lightweight polarity score; swap in your existing
transformer-based pipeline for the real submission if you want more depth.
"""
import pandas as pd

try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except ImportError:
    HAS_TEXTBLOB = False


def score_sentiment(text: str) -> float:
    if HAS_TEXTBLOB:
        return round(TextBlob(text).sentiment.polarity, 2)
    # Fallback: crude keyword scoring if textblob isn't installed
    positive_words = {"great", "excellent", "good", "amazing", "reliable", "sharp", "crisp", "fast"}
    negative_words = {"slow", "flimsy", "confusing", "issues", "hot", "loud", "expensive", "boring"}
    words = set(text.lower().replace(",", "").split())
    score = len(words & positive_words) - len(words & negative_words)
    return max(-1.0, min(1.0, score / 5))


def brand_sentiment_summary(reviews_df: pd.DataFrame) -> pd.DataFrame:
    reviews_df = reviews_df.copy()
    reviews_df["sentiment"] = reviews_df["review_text"].apply(score_sentiment)
    return (
        reviews_df.groupby("brand")["sentiment"]
        .mean()
        .round(2)
        .reset_index()
        .rename(columns={"sentiment": "avg_sentiment"})
    )


def brand_themes(reviews_df: pd.DataFrame, brand: str) -> list[str]:
    """Return the raw review snippets for a brand, used as battle-card input."""
    return reviews_df[reviews_df["brand"] == brand]["review_text"].tolist()
