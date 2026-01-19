import streamlit as st
import feedparser

# Set layout to wide to use the full width of the screen
st.set_page_config(layout="wide", page_title="GR/EU News Hub")

st.title("🗞️ News Dashboard: Greece & Europe")

# Optional Search Bar at the top
search_query = st.text_input("Search (leave blank for all top news):", "")

# Define Feeds
sources = {
    "Greece": f"https://news.google.com/rss/search?q={search_query}+Greece+news&hl=en-GR&gl=GR",
    "Europe": f"https://news.google.com/rss/search?q={search_query}+Europe+news&hl=en-150&gl=GR"
}

# 1. Create two equal columns
col1, col2 = st.columns(2)

def display_feed(container, url, label):
    feed = feedparser.parse(url)
    container.header(label)
    
    if not feed.entries:
        container.warning("No articles found.")
        return
        
    for entry in feed.entries[:10]:
        # Using markdown with standard text size for uniformity
        container.markdown(f"**[{entry.title}]({entry.link})**")
        container.caption(f"📅 {entry.published if 'published' in entry else 'Recent'}")
        container.divider()

# 2. Assign Greece to the left and Europe to the right
with col1:
    display_feed(st, sources["Greece"], "🇬🇷 Greece")

with col2:
    display_feed(st, sources["Europe"], "🇪🇺 Europe")
