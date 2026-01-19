import streamlit as st
import feedparser
from datetime import datetime

st.set_page_config(page_title="GR/EU News Hub", page_icon="🗞️")

st.title("🇪🇺 Live News: Greece & Europe")
st.caption(f"Last checked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# User Search Input
search_query = st.text_input("Search specific topics (e.g., 'Economy', 'Energy', 'Olympiacos'):", "")

# Define Feeds
sources = {
    "Greece": f"https://news.google.com/rss/search?q={search_query}+Greece+news&hl=en-GR&gl=GR",
    "Europe": f"https://news.google.com/rss/search?q={search_query}+Europe+news&hl=en-150&gl=GR"
}

tab1, tab2 = st.tabs(["🇬🇷 Greece", "🇪🇺 Europe"])

def display_feed(url):
    feed = feedparser.parse(url)
    if not feed.entries:
        st.warning("No news found for this search.")
    for entry in feed.entries[:12]:
        with st.container():
            st.markdown(f"### [{entry.title}]({entry.link})")
            st.write(f"📅 {entry.published if 'published' in entry else 'Just now'}")
            st.divider()

with tab1:
    display_feed(sources["Greece"])

with tab2:
    display_feed(sources["Europe"])
