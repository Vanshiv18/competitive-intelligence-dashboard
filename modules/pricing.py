"""
Module 2: Pricing Benchmark (PFV - Price/Family/Variant style)
Maps to JD bullet: "pricing benchmarks (PFV)"
"""
import pandas as pd


def price_band_summary(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """Where does each brand sit across Budget/Mid/Premium bands for a category."""
    cat_df = df[df["category"] == category]
    pivot = (
        cat_df.groupby(["segment", "brand"])["price_inr"]
        .mean()
        .round(0)
        .unstack(fill_value=None)
    )
    # Keep a sensible segment order if present
    order = [s for s in ["Budget", "Mid", "Premium"] if s in pivot.index]
    return pivot.reindex(order)


def price_gap_vs_hp(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """For each competitor, average price gap (%) vs HP within the same segment."""
    cat_df = df[df["category"] == category]
    seg_avg = cat_df.groupby(["segment", "brand"])["price_inr"].mean().reset_index()
    hp_avg = seg_avg[seg_avg["brand"] == "HP"].set_index("segment")["price_inr"]

    rows = []
    for _, row in seg_avg.iterrows():
        if row["brand"] == "HP" or row["segment"] not in hp_avg.index:
            continue
        hp_price = hp_avg[row["segment"]]
        gap_pct = round((row["price_inr"] - hp_price) / hp_price * 100, 1)
        rows.append(
            {
                "segment": row["segment"],
                "competitor": row["brand"],
                "competitor_price": round(row["price_inr"], 0),
                "hp_price": round(hp_price, 0),
                "gap_pct_vs_hp": gap_pct,
            }
        )
    return pd.DataFrame(rows)
