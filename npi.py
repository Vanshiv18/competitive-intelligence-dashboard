
"""
Module 5: Product Lifecycle / NPI Gap Finder
Identifies potential product gaps using price segments and competitor coverage.
"""

import pandas as pd


def find_gaps(
    df: pd.DataFrame,
    category: str,
    n_clusters: int = 4
) -> pd.DataFrame:

    cat_df = df[
        df["category"].astype(str).str.lower()
        == str(category).lower()
    ].copy()

    if cat_df.empty:
        return pd.DataFrame()

    required_columns = ["brand", "price_inr"]

    if not all(col in cat_df.columns for col in required_columns):
        return pd.DataFrame()

    cat_df["price_inr"] = pd.to_numeric(
        cat_df["price_inr"], errors="coerce"
    )

    cat_df = cat_df.dropna(subset=["price_inr"])

    if cat_df.empty:
        return pd.DataFrame()

    # Define transparent price segments
    def price_segment(price):
        if price < 50000:
            return "Budget (<₹50K)"
        elif price < 80000:
            return "Mid-Range (₹50K–₹80K)"
        elif price < 120000:
            return "Premium (₹80K–₹120K)"
        else:
            return "High-End (₹120K+)"

    cat_df["price_segment"] = cat_df["price_inr"].apply(
        price_segment
    )

    summary = (
        cat_df.groupby("price_segment")
        .agg(
            avg_price=("price_inr", "mean"),
            min_price=("price_inr", "min"),
            max_price=("price_inr", "max"),
            sku_count=("brand", "count"),
            brands_present=("brand", lambda x: sorted(set(x)))
        )
        .round(0)
        .reset_index()
    )

    summary["hp_present"] = summary["brands_present"].apply(
        lambda brands: "HP" in brands
    )

    summary["competitor_count"] = summary[
        "brands_present"
    ].apply(
        lambda brands: len([b for b in brands if b != "HP"])
    )

    summary["npi_opportunity"] = (
        (~summary["hp_present"])
        & (summary["competitor_count"] > 0)
    )

    summary["opportunity_reason"] = summary.apply(
        lambda row:
        "Competitor presence without HP coverage"
        if row["npi_opportunity"]
        else "HP coverage exists or no competitor coverage",
        axis=1
    )

    return summary.sort_values(
        ["npi_opportunity", "avg_price"],
        ascending=[False, True]
    ).reset_index(drop=True)
