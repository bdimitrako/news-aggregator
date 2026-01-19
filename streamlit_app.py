import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from itertools import zip_longest

# 1. Config & Styling
st.set_page_config(layout="wide", page_title="GR/EU News Dashboard")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .news-row { padding: 12px; border-radius: 8px; margin-bottom: 8px; min-height: 110px; }
    .even-row { background-color: #161b22; border: 1px solid #30363d; }
    .odd-row { background-color: #0d1117; }
    .timestamp { font-size: 0.8rem; color: #8b949e; font-family: monospace; }
    .news-title { font-size: 1.05rem; font-weight: 600; text-decoration: none; color: #58a6ff !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Timezone Setup
athens_tz = pytz.timezone('Europe/Athens')

def format_date_athens(struct_time):
    """Converts RSS struct_time to a localized Athens string."""
    if not struct_time:
        return "Recently"
    # RSS feeds are in UTC, so we create a UTC datetime first
    dt_utc = datetime(*struct_time[:6], tzinfo=pytz.utc)
    # Convert to Athens time
    dt_athens = dt_utc.astimezone(athens_tz)
    # Format: ddd, dd mmm yyyy hh:mm (e.g., Mon, 19 Jan 2026 17:30)
    return dt_athens.strftime("%a, %d %b %Y %H:%M")

# 3. Header & Search
current_time = datetime.now(athens_tz).strftime("%H:%M:%S")
st.title("🗞️ News Hub: Greece & Europe")
st.caption(f"Athens Local Time: {current_time}")

search_query = st.text_input("🔍 Search topics", placeholder="Type and press Enter...")
safe_query = urllib.parse.quote_plus(search_query)

# 4. Fetch Data
sources = {
    "Greece": f"https://news.google.com/rss/search?q={safe_query}+Greece+news&hl=en-GR&gl=GR",
    "Europe": f"https://news.google.com/rss/search?q={safe_query}+Europe+news&hl=en-150&gl=GR"
}

feed_gr = feedparser.parse(sources["Greece"]).entries[:12]
feed_eu = feedparser.parse(sources["Europe"]).entries[:12]

st.markdown("---")
h_col1, h_col2 = st.columns(2)
h_col1.subheader("🇬🇷 Greece")
h_col2.subheader("🇪🇺 Europe")

# 5. The Grid
for i, (gr, eu) in enumerate(zip_longest(feed_gr, feed_eu)):
    row_class = "even-row" if i % 2 == 0 else "odd-row"
    col1, col2 = st.columns(2)
    
    with col1:
        if gr:
            time_str = format_date_athens(gr.get('published_parsed'))
            st.markdown(f"""<div class='news-row {row_class}'>
                <a class='news-title' href='{gr.link}' target='_blank'>{gr.title}</a><br>
                <span class='timestamp'>🕒 {time_str}</span>
                </div>""", unsafe_allow_html=True)

    with col2:
        if eu:
            time_str = format_date_athens(eu.get('published_parsed'))
            st.markdown(f"""<div class='news-row {row_class}'>
                <a class='news-title' href='{eu.link}' target='_blank'>{eu.title}</a><br>
                <span class='timestamp'>🕒 {time_str}</span>
                </div>""", unsafe_allow_html=True)