import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from itertools import zip_longest
from newspaper import Article
import requests
import base64
import re

# 1. Config & Styling
st.set_page_config(layout="wide", page_title="News Hub", page_icon="🗞️")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-left: 1rem !important; padding-right: 1rem !important; }
    .news-row { padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #30363d; background-color: #161b22; }
    .timestamp { font-size: 0.8rem; color: #8b949e; font-family: monospace; }
    .news-title { font-size: 1.1rem; font-weight: 600; text-decoration: none; color: #58a6ff !important; line-height: 1.4; }
    .preview-box { background-color: #0d1117; padding: 10px; border-radius: 5px; border-left: 3px solid #58a6ff; margin-top: 10px; font-size: 0.95rem; }
    </style>
""", unsafe_allow_html=True)

# 2. Advanced URL Decoder & Scraper
@st.cache_data(ttl=3600)
def get_clean_preview(google_url):
    try:
        # Step A: Decode Google's Base64 URL if possible
        url = google_url
        if "articles/" in google_url:
            try:
                base64_str = google_url.split("articles/")[1].split("?")[0]
                decoded_bytes = base64.urlsafe_b64decode(base64_str + '==')
                match = re.search(rb'https?://[^\s<>"]+', decoded_bytes)
                if match:
                    url = match.group().decode('utf-8')
            except:
                pass

        # Step B: Fetch with Browser Headers
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        
        # Step C: Parse Content
        article = Article(url)
        article.download(input_html=response.text)
        article.parse()
        
        if len(article.text) < 100:
            return "⚠️ Content is protected by the publisher. Click 'Source Link' to read."
        return article.text[:600] + "..."
    except:
        return "❌ Technical block: This site prevents automated reading."

# 3. Language Setup
lang_options = {
    "English": {"title": "🗞️ News Hub", "greece": "🇬🇷 Greece", "europe": "🇪🇺 Europe", "read": "Read Preview", "load_full": "Fetch Full Text", "gr_lang": "en-GR", "gr_gl": "GR"},
    "Ελληνικά": {"title": "🗞️ Ενημέρωση", "greece": "🇬🇷 Ελλάδα", "europe": "🇪🇺 Ευρώπη", "read": "Προεπισκόπηση", "load_full": "Ανάκτηση Κειμένου", "gr_lang": "el", "gr_gl": "GR"}
}
selected_lang = st.sidebar.selectbox("Language / Γλώσσα", ["English", "Ελληνικά"])
L = lang_options[selected_lang]

# 4. Fetch Data
search_query = st.text_input("🔍 Search / Αναζήτηση", "")
safe_query = urllib.parse.quote_plus(search_query)

sources = {
    "Greece": f"https://news.google.com/rss/search?q={safe_query}+Greece&hl={L['gr_lang']}&gl={L['gr_gl']}",
    "Europe": f"https://news.google.com/rss/search?q={safe_query}+Europe&hl=en-150&gl=GR"
}

feed_gr = feedparser.parse(sources["Greece"]).entries[:10]
feed_eu = feedparser.parse(sources["Europe"]).entries[:10]

# 5. UI Grid
st.title(L["title"])
col_gr, col_eu = st.columns(2)

def render_news_item(entry, key_prefix):
    if not entry: return
    with st.container():
        st.markdown(f"<div class='news-row'><a class='news-title' href='{entry.link}' target='_blank'>{entry.title}</a></div>", unsafe_allow_html=True)
        
        with st.expander(L["read"]):
            # Stage 1: The RSS Summary (Works 100% of the time)
            rss_summary = re.sub('<[^<]+?>', '', entry.get('summary', ''))
            st.markdown(f"<div class='preview-box'><b>Quick Snippet:</b><br>{rss_summary}</div>", unsafe_allow_html=True)
            
            # Stage 2: The Deep Scraper (Optional button)
            if st.button(L["load_full"], key=f"{key_prefix}_{entry.link}"):
                with st.spinner("Decoding & Fetching..."):
                    full_text = get_clean_preview(entry.link)
                    st.write(full_text)
            st.markdown(f"🔗 [Source Link]({entry.link})")

with col_gr:
    st.subheader(L["greece"])
    for i, item in enumerate(feed_gr): render_news_item(item, f"gr_{i}")

with col_eu:
    st.subheader(L["europe"])
    for i, item in enumerate(feed_eu): render_news_item(item, f"eu_{i}")