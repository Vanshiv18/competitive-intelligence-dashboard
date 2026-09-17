"""
CompIntel - Competitive Intelligence & Battle Card Engine
A market research / competitive intelligence tool built around the
laptop & printer categories, mirroring an HP Market Research &
Intelligence Intern's core deliverables.

Run locally:   streamlit run app.py
Deploy:        push to GitHub, connect repo at share.streamlit.io
"""
import streamlit as st
import pandas as pd

import kpi
import pricing
import sentiment
import npi
import battlecards

st.set_page_config(page_title="CompIntel", layout="wide")


# ---- Professional Styling ----
st.markdown("""
<style>
    .stApp {
        background-color: #f4f7fb;
    }

    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #123c69;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 16px;
        color: #52616b;
        margin-bottom: 25px;
    }

    [data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #dce6f2;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }

    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 15px;
    }

    h1, h2, h3 {
        color: #123c69;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">CompIntel | Competitive Intelligence Hub</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Market Intelligence • Pricing Analytics • Competitor Strategy • NPI Insights</div>',
    unsafe_allow_html=True
)

st.caption(
    "Category KPIs · Pricing Benchmarks (PFV) · Competitor Sentiment · "
    "Auto Battle Cards · NPI Gap Finder"
)

# ---- Load Data + CSV Upload ----
st.sidebar.markdown("## 📂 Data Management")

uploaded_file = st.sidebar.file_uploader(
    "Upload Competitor CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"Uploaded {len(df)} products")
else:
    df = kpi.load_data("data/dashboard_competitor_data.csv")

# ---- Data Validation ----
required_columns = ["brand", "category", "price_inr"]
missing_columns = [c for c in required_columns if c not in df.columns]

if missing_columns:
    st.error("Missing columns: " + ", ".join(missing_columns))
    st.stop()

duplicate_count = int(df.duplicated().sum())

if duplicate_count > 0:
    st.warning(f"Duplicate records detected: {duplicate_count}")

st.sidebar.info(f"Validated records: {len(df)}")

# ---- Export Data ----
st.sidebar.markdown("## 📥 Export Data")

csv_export = df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="⬇️ Download Competitor CSV",
    data=csv_export,
    file_name="competitor_data_export.csv",
    mime="text/csv"
)

reviews_df = pd.DataFrame(columns=["brand", "review_text"])



# ---- Interactive Sidebar Filters ----
with st.sidebar:
    st.markdown("## 🎯 Dashboard Filters")
    st.markdown("Customize your competitive intelligence view.")

    selected_brands = st.multiselect(
        "Select Brands",
        sorted(df["brand"].dropna().unique()),
        default=sorted(df["brand"].dropna().unique())
    )

    selected_categories = st.multiselect(
        "Select Categories",
        sorted(df["category"].dropna().unique()),
        default=sorted(df["category"].dropna().unique())
    )

    min_price = int(df["price_inr"].min())
    max_price = int(df["price_inr"].max())

    price_range = st.slider(
        "Price Range (₹)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=1000
    )

filtered_df = df[
    (df["brand"].isin(selected_brands)) &
    (df["category"].isin(selected_categories)) &
    (df["price_inr"].between(price_range[0], price_range[1]))
].copy()

df = filtered_df


# ---- Professional Company Header ----
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0b1f3a, #1565c0, #42a5f5);
    padding: 28px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
">
    <h1 style="color:white; margin:0;">
        🏢 CompIntel
    </h1>
    <h3 style="color:#e3f2fd; margin-top:8px;">
        Competitive Intelligence & Market Analytics Hub
    </h3>
    <p style="color:#e3f2fd;">
        Product Intelligence • Pricing Strategy • Customer Sentiment • NPI Insights
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🖥️ Product Intelligence Showcase")

showcase_cols = st.columns(3)

product_showcase = [
    ("💻", "Laptop Intelligence", "Compare competitor configurations and pricing"),
    ("🖨️", "Printer Intelligence", "Analyze category-level market positioning"),
    ("📈", "Market Analytics", "Identify pricing gaps and product opportunities")
]

for col, (icon, title, description) in zip(showcase_cols, product_showcase):
    with col:
        st.markdown(f"""
        <div style="
            background:white;
            padding:22px;
            border-radius:15px;
            border:1px solid #dce6f2;
            min-height:145px;
            box-shadow:0 4px 12px rgba(0,0,0,0.06);
        ">
            <h2>{icon}</h2>
            <h4 style="color:#123c69;">{title}</h4>
            <p style="color:#52616b;">{description}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ---- Executive KPI Cards ----
total_products = len(df)
total_brands = df["brand"].nunique()
avg_price = df["price_inr"].mean()
avg_rating = df["rating"].mean() if df["rating"].notna().any() else None

st.markdown("### Executive Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Products", total_products)

with col2:
    st.metric("Brands Tracked", total_brands)

with col3:
    st.metric("Average Price", f"₹{avg_price:,.0f}")

with col4:
    st.metric("Average Rating", f"{avg_rating:.2f} ⭐" if avg_rating is not None else "N/A")

st.markdown("---")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["KPI Overview", "Pricing Benchmark", "Sentiment & Positioning", "Battle Cards", "NPI Gaps", "Market Insights"]
)

# ---- Tab 1: Category KPIs ----
with tab1:
    st.subheader("Category KPI Tracker")
    kpi_table = kpi.category_kpis(df)

    # Professional display for missing values
    kpi_display = kpi_table.copy()

    display_columns = [
        "avg_rating",
        "total_reviews",
        "avg_discount_pct"
    ]

    for col in display_columns:
        if col in kpi_display.columns:
            kpi_display[col] = kpi_display[col].fillna("N/A")

    st.dataframe(kpi_display, use_container_width=True)

    # Keep numerical data for charting
    st.bar_chart(
        kpi_table,
        x="brand",
        y="avg_price",
        color="category"
    )

# ---- Tab 2: Pricing Benchmark ----
with tab2:
    st.subheader("Pricing Benchmark (PFV)")
    category = st.selectbox("Category", df["category"].unique(), key="pricing_cat")
    st.write("Average price by segment and brand:")
    st.dataframe(pricing.price_band_summary(df, category), use_container_width=True)
    st.write("Price gap vs HP:")
    st.dataframe(pricing.price_gap_vs_hp(df, category), use_container_width=True)

# ---- Tab 3: Sentiment & Positioning ----
with tab3:
    st.subheader("Competitor Sentiment & Positioning")

    if reviews_df.empty:
        sent_summary = pd.DataFrame(
            columns=["brand", "avg_sentiment"]
        )

        st.info(
            "Review data is currently unavailable. "
            "Verified competitor reviews are required "
            "before sentiment analysis can be displayed."
        )

    else:
        sent_summary = sentiment.brand_sentiment_summary(
            reviews_df
        )

        st.dataframe(
            sent_summary,
            use_container_width=True
        )

        st.bar_chart(
            sent_summary,
            x="brand",
            y="avg_sentiment"
        )

# ---- Tab 4: Battle Cards ----
with tab4:
    st.subheader("Auto-Generated Battle Cards")
    category = st.selectbox("Category", df["category"].unique(), key="battle_cat")
    competitors = [b for b in df[df["category"] == category]["brand"].unique() if b != "HP"]
    competitor = st.selectbox("Competitor", competitors)

    gap_df = pricing.price_gap_vs_hp(df, category)
    gap_row = gap_df[gap_df["competitor"] == competitor]

    if not gap_row.empty:
        gap = gap_row.iloc[0].to_dict()
        sent_row = sent_summary[sent_summary["brand"] == competitor]
        sent_score = sent_row["avg_sentiment"].iloc[0] if not sent_row.empty else 0.0
        themes = sentiment.brand_themes(reviews_df, competitor)

        if st.button(f"Generate battle card for {competitor}"):
            card = battlecards.generate_battlecard(competitor, gap, sent_score, themes)
            st.text(card)
    else:
        st.info("No overlapping segment data for this competitor in this category.")

# ---- Tab 5: NPI Gap Finder ----
with tab5:
    st.subheader("Product Lifecycle / NPI Gap Finder")

    st.caption(
        "Identifies price segments where competitors are present "
        "but HP has no listed product in the current dataset."
    )

    category = st.selectbox(
        "Select Category",
        sorted(df["category"].dropna().unique()),
        key="npi_cat"
    )

    gaps = npi.find_gaps(df, category)

    if gaps.empty:
        st.info("No sufficient data available for NPI gap analysis.")
    else:
        opportunities = gaps[gaps["npi_opportunity"]].copy()

        col1, col2, col3 = st.columns(3)

        col1.metric("Segments Analysed", len(gaps))
        col2.metric("Potential Coverage Gaps", len(opportunities))
        col3.metric(
            "HP Covered Segments",
            int(gaps["hp_present"].sum())
        )

        st.markdown("### 📊 Segment Coverage Analysis")

        display_cols = [
            "price_segment",
            "avg_price",
            "min_price",
            "max_price",
            "sku_count",
            "brands_present",
            "hp_present",
            "competitor_count",
            "npi_opportunity",
            "opportunity_reason"
        ]

        display_cols = [
            col for col in display_cols if col in gaps.columns
        ]

        st.dataframe(
            gaps[display_cols],
            use_container_width=True,
            hide_index=True
        )

        if not opportunities.empty:
            st.warning(
                f"⚠️ {len(opportunities)} potential coverage gap(s) "
                "identified in the current dataset."
            )

            st.markdown("### 🎯 Potential NPI Coverage Areas")

            st.dataframe(
                opportunities[
                    [
                        col for col in [
                            "price_segment",
                            "avg_price",
                            "min_price",
                            "max_price",
                            "brands_present",
                            "opportunity_reason"
                        ]
                        if col in opportunities.columns
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            npi_csv = opportunities.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇️ Download NPI Gap Report",
                data=npi_csv,
                file_name="npi_gap_report.csv",
                mime="text/csv"
            )
        else:
            st.success(
                "No uncovered price segments detected "
                "for HP in the current dataset."
            )


# ---- Tab 6: Market Insights ----
with tab6:
    st.subheader("Market Insights")

    st.caption(
        "Analytical insights based on the current product sample. "
        "These figures do not represent total market share."
    )

    # KPI metrics
    total_products = len(df)
    total_brands = df["brand"].nunique()
    average_price = df["price_inr"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Products Analysed", total_products)
    col2.metric("Brands Compared", total_brands)
    col3.metric("Average Listed Price", f"₹{average_price:,.0f}")

    st.divider()

    # Brand-level analysis
    st.subheader("Brand Price Comparison")

    brand_summary = (
        df.groupby("brand")
        .agg(
            Product_Count=("model", "count"),
            Average_Price=("price_inr", "mean"),
            Minimum_Price=("price_inr", "min"),
            Maximum_Price=("price_inr", "max")
        )
        .reset_index()
        .sort_values("Average_Price")
    )

    st.dataframe(
        brand_summary.style.format({
            "Average_Price": "₹{:,.0f}",
            "Minimum_Price": "₹{:,.0f}",
            "Maximum_Price": "₹{:,.0f}"
        }),
        use_container_width=True
    )

    st.bar_chart(
        brand_summary.set_index("brand")["Average_Price"],
        use_container_width=True
    )

    st.divider()

    # Segment distribution
    st.subheader("Product Segment Distribution")

    segment_summary = (
        df.groupby(["brand", "segment"])
        .size()
        .unstack(fill_value=0)
    )

    st.dataframe(segment_summary, use_container_width=True)

    st.bar_chart(segment_summary, use_container_width=True)

    st.divider()

    # Key observations
    st.subheader("Key Observations")

    lowest_brand = brand_summary.iloc[0]["brand"]
    highest_brand = brand_summary.iloc[-1]["brand"]

    st.markdown(f"""
    - **Sample coverage:** {total_products} products across {total_brands} brands.
    - **Lowest average listed price:** {lowest_brand}.
    - **Highest average listed price:** {highest_brand}.
    - The dataset contains products across multiple price segments.
    - These observations are based on listed prices and should not be interpreted as market-share estimates.
    """)
