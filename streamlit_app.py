import streamlit as st
import feedparser
from datetime import datetime
import pytz

# 1. Dashboard Config
st.set_page_config(layout="wide", page_title="GR/EU News Dashboard")

# 2. Inject CSS for tight spacing and custom row colors
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    .news-row { padding: 10px; border-radius: 5px; margin-bottom: 5px; }
    .even-row { background-color: #0e1117; } /* Standard Dark */
    .odd-row { background-color: #1a1c24; }  /* Slightly Lighter */
    .timestamp { font-size: 0.8rem; color: #808495; }
    </style>
""", unsafe_allow_html=True)

greece_tz = pytz.timezone('Europe/Athens')
current_time = datetime.now(greece_tz).strftime("%H:%M:%S")

st.title("🗞️ Real-Time News Hub")
st.caption(f"Athens Local Time: {current_time}")

# 3. Data Fetching
sources = {
    "Greece": "https://news.google.com/rss/search?q=Greece+news&hl=en-GR&gl=GR",
    "Europe": "https://news.google.com/rss/search?q=Europe+news&hl=en-150&gl=GR"
}

feed_gr = feedparser.parse(sources["Greece"]).entries[:12]
feed_eu = feedparser.parse(sources["Europe"]).entries[:12]

# 4. Header Row
h_col1, h_col2 = st.columns(2)
h_col1.subheader("🇬🇷 Greece Headlines")
h_col2.subheader("🇪🇺 Europe Headlines")

# 5. Iterating Grid with Alternating Colors
for i, (gr, eu) in enumerate(zip(feed_gr, feed_eu)):
    # Toggle color class based on row index
    row_class = "even-row" if i % 2 == 0 else "odd-row"
    
    # Create a single row container
    with st.container():
        col1, col2 = st.columns(2)
        
        # Greece Column
        with col1:
            st.markdown(f"""<div class='news-row {row_class}'>
                <a href='{gr.link}' style='text-decoration:none; color:white; font-weight:bold;'>{gr.title}</a><br>
                <span class='timestamp'>🕒 Posted: {gr.published if 'published' in gr else 'Recently'}</span>
                </div>""", unsafe_allow_html=True)

        # Europe Column
        with col2:
            st.markdown(f"""<div class='news-row {row_class}'>
                <a href='{eu.link}' style='text-decoration:none; color:white; font-weight:bold;'>{eu.title}</a><br>
                <span class='timestamp'>🕒 Posted: {eu.published if 'published' in eu else 'Recently'}</span>
                </div>""", unsafe_allow_html=True)