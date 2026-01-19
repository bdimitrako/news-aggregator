import streamlit as st
import feedparser
from datetime import datetime
import pytz

# 1. Dashboard Config
st.set_page_config(layout="wide", page_title="GR/EU News Dashboard")

# 2. Advanced CSS: Fixed Search Bar & Alternating Row Colors
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .news-row { padding: 12px; border-radius: 8px; margin-bottom: 8px; min-height: 100px; }
    .even-row { background-color: #161b22; border: 1px solid #30363d; } /* Dark */
    .odd-row { background-color: #0d1117; } /* Slightly Lighter */
    .timestamp { font-size: 0.75rem; color: #8b949e; font-style: italic; }
    .news-title { font-size: 1.05rem; font-weight: 600; text-decoration: none; color: #58a6ff !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Timezone & Search Section
greece_tz = pytz.timezone('Europe/Athens')
current_time = datetime.now(greece_tz).strftime("%H:%M:%S")

st.title("🗞️ News Hub: Greece & Europe")
st.caption(f"Athens Local Time: {current_time}")

# --- RESTORED SEARCH BAR ---
search_query = st.text_input("🔍 Search topics (e.g. 'Economy', 'Sports', 'Energy')", placeholder="Type here and press Enter...")

# 4. Data Fetching (Integrated with Search)
# We encode the search query into the Google News RSS URL
sources = {
    "Greece": f"https://news.google.com/rss/search?q={search_query}+Greece+news&hl=en-GR&gl=GR",
    "Europe": f"https://news.google.com/rss/search?q={search_query}+Europe+news&hl=en-150&gl=GR"
}

feed_gr = feedparser.parse(sources["Greece"]).entries[:12]
feed_eu = feedparser.parse(sources["Europe"]).entries[:12]

# 5. Header Row
st.markdown("---")
h_col1, h_col2 = st.columns(2)
h_col1.subheader("🇬🇷 Greece")
h_col2.subheader("🇪🇺 Europe")

# 6. Aligned Grid with Alternating Colors
# Using zip_longest to handle cases where one feed has fewer results
from itertools import zip_longest

for i, (gr, eu) in enumerate(zip_longest(feed_gr, feed_eu)):
    row_class = "even-row" if i % 2 == 0 else "odd-row"
    col1, col2 = st.columns(2)
    
    with col1:
        if gr:
            st.markdown(f"""<div class='news-row {row_class}'>
                <a class='news-title' href='{gr.link}' target='_blank'>{gr.title}</a><br>
                <span class='timestamp'>🕒 {gr.published if 'published' in gr else 'Recently'}</span>
                </div>""", unsafe_allow_html=True)

    with col2:
        if eu:
            st.markdown(f"""<div class='news-row {row_class}'>
                <a class='news-title' href='{eu.link}' target='_blank'>{eu.title}</a><br>
                <span class='timestamp'>🕒 {eu.published if 'published' in eu else 'Recently'}</span>
                </div>""", unsafe_allow_html=True)