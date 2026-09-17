"""
Module 1: Category KPI Tracker
Maps to JD bullet: "Data Analytics: Track Category KPI's, Sales metrics"
"""
import pandas as pd


def load_data(path: str = "data/sample_products.csv") -> pd.DataFrame:
    return pd.read_csv(path)


def category_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Average price, rating, review volume and discount per brand+category."""
    return (
        df.groupby(["category", "brand"])
        .agg(
            avg_price=("price_inr", "mean"),
            avg_rating=("rating", "mean"),
            total_reviews=("review_count", "sum"),
            avg_discount_pct=("discount_pct", "mean"),
            sku_count=("model", "count"),
        )
        .round(1)
        .reset_index()
    )


def brand_scorecard(df: pd.DataFrame, brand: str) -> dict:
    """Quick single-brand snapshot used inside battle cards."""
    b = df[df["brand"] == brand]
    if b.empty:
        return {}
    return {
        "brand": brand,
        "avg_price": round(b["price_inr"].mean(), 0),
        "avg_rating": round(b["rating"].mean(), 2),
        "total_reviews": int(b["review_count"].sum()),
        "avg_discount_pct": round(b["discount_pct"].mean(), 1),
        "sku_count": int(b["model"].count()),
    }
