import streamlit as st
from database import create_db, get_mentions, insert_mention
import time
from fetcher import fetch_all
from analyzer import analyze_mention

# MUST BE FIRST
st.set_page_config(page_title="Brand Monitor", page_icon="📡", layout="wide")

create_db()

if "current_brand" not in st.session_state:
    st.session_state.current_brand = ""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], p, h1, h2, h3, h4, h5, h6, 
span:not(.material-icons-sharp), div, input, button, select, textarea {
    font-family: 'Space Grotesk', sans-serif !important;
}
.stApp { background: #0a0a0f; color: #e0e0e0; }
[data-testid="stSidebar"] { background: #0f0f1a !important; border-right: 1px solid #1e1e2e; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
input, textarea, select { background: #1a1a2e !important; color: #e0e0e0 !important; border: 1px solid #2e2e4e !important; border-radius: 8px !important; }
.stButton > button { background: linear-gradient(135deg, #6c63ff, #3ecfcf) !important; color: white !important; border: none !important; border-radius: 10px !important; padding: 0.6rem 1.5rem !important; font-weight: 600 !important; width: 100% !important; }
.stButton > button:hover { box-shadow: 0 8px 25px rgba(108, 99, 255, 0.4) !important; }
[data-testid="stMetric"] { background: #12121f; border: 1px solid #1e1e3f; border-radius: 12px; padding: 1rem; text-align: center; }
[data-testid="stMetricValue"] { color: #6c63ff !important; font-size: 2rem !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #888 !important; font-size: 0.8rem !important; text-transform: uppercase; letter-spacing: 0.1em; }
hr { border-color: #1e1e3f !important; }
[data-testid="stSelectbox"] > div > div { background: #1a1a2e !important; border: 1px solid #2e2e4e !important; border-radius: 8px !important; color: #e0e0e0 !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2e2e4e; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #6c63ff; }
@keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
.brand-title { font-size: 2.8rem; font-weight: 700; background: linear-gradient(135deg, #6c63ff, #3ecfcf, #ff6584, #6c63ff); background-size: 300% 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: gradientShift 4s ease infinite; margin-bottom: 0.2rem; }
.subtitle { color: #555; font-size: 0.95rem; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 2rem; }
.badge { display: inline-block; padding: 3px 12px; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }
.badge-positive { background: #0d2b1e; color: #3ecf8e; border: 1px solid #1a5c3a; }
.badge-negative { background: #2b0d0d; color: #ff6584; border: 1px solid #5c1a1a; }
.badge-neutral  { background: #1a1a2e; color: #aaa; border: 1px solid #2e2e4e; }
.score-bar-bg { background: #1a1a2e; border-radius: 999px; height: 6px; width: 100%; margin-top: 4px; }
.score-bar-fill { height: 6px; border-radius: 999px; background: linear-gradient(90deg, #6c63ff, #3ecfcf); }
.source-hn { background:#1f1200; color:#ff9900; border:1px solid #3d2600; padding:2px 10px; border-radius:999px; font-size:0.72rem; font-weight:600; }
.source-news { background:#001a2e; color:#3ecfcf; border:1px solid #003d5c; padding:2px 10px; border-radius:999px; font-size:0.72rem; font-weight:600; }
.stat-row { display:flex; align-items:center; gap:12px; margin:6px 0; font-size:0.85rem; }
.stat-label { width:70px; color:#888; }
.stat-track { flex:1; background:#1a1a2e; border-radius:999px; height:8px; }
.stat-fill { height:8px; border-radius:999px; }
.stat-count { width:30px; text-align:right; color:#555; font-size:0.8rem; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="brand-title">📡 Brand Monitor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-time brand intelligence powered by local AI</div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")
    brand = st.text_input("Brand / Keyword", value=st.session_state.current_brand, placeholder="e.g. Tesla, Apple...")
    st.markdown("**Data Sources**")
    st.checkbox("HackerNews", value=True)
    st.checkbox("NewsAPI", value=True)
    st.markdown("---")

    if st.button("🚀 Fetch & Analyze"):
        if brand:
            brand = brand.strip().title()
            st.session_state.current_brand = brand
            progress_text = st.empty()

            progress_text.markdown("🗑️ Clearing old data...")
            # delete old mentions for this brand
            import sqlite3
            conn = sqlite3.connect("brand_monitor.db")
            conn.execute("DELETE FROM mentions WHERE LOWER(brand) = LOWER(?)", (brand,))
            conn.commit()
            conn.close()

            progress_text.markdown("⏳ Fetching fresh mentions...")
            mentions_raw = fetch_all(brand)
            total = len(mentions_raw)
            progress_text.markdown(f"✅ Fetched **{total} mentions**. Analyzing...")

            for i, mention in enumerate(mentions_raw):
                progress_text.markdown(f"🧠 Analyzing **{i+1} / {total}**: {mention['title'][:40]}...")
                try:
                    analysis = analyze_mention(mention["title"], mention["content"])
                    insert_mention(
                        brand=brand,
                        source=mention["source"],
                        title=mention["title"],
                        content=mention["content"],
                        url=mention["url"],
                        sentiment=analysis["sentiment"],
                        score=analysis["score"]
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    continue
                time.sleep(0.5)

            progress_text.markdown(f"✅ Done! **{total} mentions** analyzed and saved.")
            time.sleep(1)
            st.rerun()
        else:
            st.warning("Please enter a brand name first.")

    st.markdown("---")
    st.markdown('<p style="color:#333;font-size:0.75rem;text-align:center;">Powered by Groq + Mistral</p>', unsafe_allow_html=True)

# MAIN CONTENT
# get brand from session state OR from the input box
active_brand = st.session_state.current_brand or brand
mentions = get_mentions(active_brand) if active_brand else []
st.write(f"DEBUG: '{active_brand}' → {len(mentions)} results")

if not mentions:
    st.markdown("""
    <div style="text-align:center;padding:4rem 0;color:#333;">
        <div style="font-size:3rem">📭</div>
        <div style="font-size:1.1rem;margin-top:1rem;color:#555">No data yet.</div>
        <div style="font-size:0.85rem;margin-top:0.5rem;color:#444">Enter a brand name and click Fetch & Analyze</div>
    </div>
    """, unsafe_allow_html=True)
else:
    total    = len(mentions)
    positive = len([m for m in mentions if m["sentiment"] == "positive"])
    negative = len([m for m in mentions if m["sentiment"] == "negative"])
    neutral  = len([m for m in mentions if m["sentiment"] == "neutral"])
    avg_score = round(sum(m["score"] for m in mentions) / total, 1)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Mentions", total)
    c2.metric("Avg Score", f"{avg_score}/10")
    c3.metric("Positive", positive)
    c4.metric("Negative", negative)
    c5.metric("Neutral", neutral)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown("#### Sentiment Breakdown")
        pos_pct = round((positive / total) * 100)
        neg_pct = round((negative / total) * 100)
        neu_pct = round((neutral  / total) * 100)
        st.markdown(f"""
        <div class="stat-row">
            <div class="stat-label">Positive</div>
            <div class="stat-track"><div class="stat-fill" style="width:{pos_pct}%;background:#3ecf8e"></div></div>
            <div class="stat-count">{positive}</div>
        </div>
        <div class="stat-row">
            <div class="stat-label">Neutral</div>
            <div class="stat-track"><div class="stat-fill" style="width:{neu_pct}%;background:#888"></div></div>
            <div class="stat-count">{neutral}</div>
        </div>
        <div class="stat-row">
            <div class="stat-label">Negative</div>
            <div class="stat-track"><div class="stat-fill" style="width:{neg_pct}%;background:#ff6584"></div></div>
            <div class="stat-count">{negative}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("#### All Mentions")

        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            filter_sentiment = st.selectbox("Filter by sentiment", ["All", "positive", "negative", "neutral"])
        with filter_col2:
            filter_source = st.selectbox("Filter by source", ["All", "hackernews", "newsapi"])

        filtered = mentions
        if filter_sentiment != "All":
            filtered = [m for m in filtered if m["sentiment"] == filter_sentiment]
        if filter_source != "All":
            filtered = [m for m in filtered if m["source"] == filter_source]

        for m in filtered:
            badge_class = f"badge-{m['sentiment']}"
            source_class = "source-hn" if m["source"] == "hackernews" else "source-news"
            source_label = "HN" if m["source"] == "hackernews" else "NEWS"
            score_pct = int((m["score"] / 10) * 100)

            st.markdown(f"""
            <div style="background:#12121f;border:1px solid #1e1e3f;border-radius:12px;padding:1rem 1.25rem;margin-bottom:0.75rem;">
                <div style="font-size:0.9rem;color:#e0e0e0;margin-bottom:10px;line-height:1.4;">{m['title']}</div>
                <div style="display:flex;gap:10px;align-items:center;margin-bottom:10px;">
                    <span class="{source_class}">{source_label}</span>
                    <span class="badge {badge_class}">{m['sentiment']}</span>
                    <span style="font-size:0.75rem;color:#555">{m['fetched_at'][:10]}</span>
                </div>
                <div style="font-size:0.75rem;color:#555;margin-bottom:4px;">Score: {m['score']}/10</div>
                <div class="score-bar-bg"><div class="score-bar-fill" style="width:{score_pct}%"></div></div>
                <div style="margin-top:10px;">
                    <a href="{m['url']}" target="_blank" style="color:#6c63ff;font-size:0.78rem;text-decoration:none;">View source →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)