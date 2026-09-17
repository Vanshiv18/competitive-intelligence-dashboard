"""
Module 4: Battle Card Generator
Maps to JD bullet: "preparation of battle cards, creating the value prop"

Uses the Anthropic API if ANTHROPIC_API_KEY is set in the environment.
Falls back to a rule-based template so the app still works with zero API
cost during development/demo (important for a live free-tier deployment).
"""
import os

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


def _template_battlecard(competitor: str, price_gap: dict, sentiment_score: float, themes: list[str]) -> str:
    price_line = (
        f"{competitor} is priced {abs(price_gap['gap_pct_vs_hp'])}% "
        f"{'above' if price_gap['gap_pct_vs_hp'] > 0 else 'below'} HP in the {price_gap['segment']} segment."
    )
    if themes:
        tone = (
            "generally positive"
            if sentiment_score > 0.1
            else "generally negative"
            if sentiment_score < -0.1
            else "mixed"
        )
        sentiment_line = f"Customer sentiment: {tone} (score {sentiment_score})"
        themes_line = " | ".join(themes[:3])
        counter_pitch = (
            "Review customer feedback themes before making "
            "sentiment-based sales claims."
        )
    else:
        sentiment_line = "Customer sentiment: Data unavailable"
        themes_line = "No verified review data available."
        counter_pitch = (
            "Use verified pricing and product specifications. "
            "Do not make sentiment-based competitor claims "
            "until review data is collected."
        )

    return f"""BATTLE CARD: {competitor}
--------------------------------
PRICE POSITIONING
{price_line}

CUSTOMER SENTIMENT
{sentiment_line}
Sample signals: {themes_line}

SUGGESTED HP COUNTER-PITCH
{counter_pitch}
"""


def generate_battlecard(
    competitor: str,
    price_gap: dict,
    sentiment_score: float,
    themes: list[str],
) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not (HAS_ANTHROPIC and api_key):
        return _template_battlecard(competitor, price_gap, sentiment_score, themes)

    client = anthropic.Anthropic(api_key=api_key)
    prompt = f"""Create a concise sales battle card comparing HP against {competitor}.

Price data: {competitor} is {price_gap['gap_pct_vs_hp']}% vs HP in the {price_gap['segment']} segment.
Customer sentiment score for {competitor}: {sentiment_score} (range -1 to 1).
Sample review signals: {themes[:5]}

Return four short sections: STRENGTHS (competitor's), WEAKNESSES (competitor's),
PRICE POSITIONING, RECOMMENDED VALUE PROP for HP sales reps to use. Keep it under 150 words."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
