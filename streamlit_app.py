import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import requests
import base64
import re
from itertools import zip_longest
from newspaper import Article

# 1. Config & Styling
# We keep layout="wide" for desktop but CSS will handle mobile wrapping
st.set_page_config(layout="wide", page_title="News Hub", page_icon="🗞️")

st.markdown("""
    <style>
    /* Improve padding for mobile */
    .block-container { 
        padding-top: 2rem; 
        padding-left: 1rem !important; 
        padding-right: 1rem !important; 
    }
    
    /* Card-like styling for news rows */
    .news-row { 
        padding: 15px; 
        border-radius: 10px; 
        margin-bottom: 10px; 
        transition: transform 0.2s;
    }
    .even-row { background-color: #161b22; border: 1px solid #30363d; }
    .odd-row { background-color: #0d1117; border: 1px solid #21262d; }
    
    /* Typography */
    .timestamp { font-size: 0.8rem; color: #8b949e; font-family: monospace; }
    .news-title { 
        font-size: 1.1rem; 
        font-weight: 600; 
        text-decoration: none; 
        color: #58a6ff !important; 
        line-height: 1.4;
    }
    
    /* Mobile adjustments: Stack columns better if needed */
    @media (max-width: 640px) {
        .news-title { font-size: 1rem; }
    }
    </style>
""", unsafe_allow_html=True)

# 2. Helper Functions
@st.cache_data(ttl=3600)
def get_article_preview(google_url):
    try:
        # 1. Decode the Google "masked" URL to find the real source
        # Google News RSS links often contain the real URL base64 encoded
        if "articles/" in google_url:
            suffix = google_url.split("articles/")[1].split("?")[0]
            # This is a common pattern for Google News base64 encoding
            try:
                # We try to pad the string to make it valid base64
                decoded_bytes = base64.urlsafe_b64decode(suffix + '==')
                # Use regex to find the first string that looks like a URL
                match = re.search(rb'https?://[^\s<>"]+', decoded_bytes)
                if match:
                    url = match.group().decode('utf-8')
                else:
                    url = google_url
            except:
                url = google_url
        else:
            url = google_url

        # 2. Fetch with a "Real Browser" header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        
        # 3. Download and Parse
        article = Article(url)
        article.download(input_html=requests.get(url, headers=headers, timeout=10).text)
        article.parse()
        
        if len(article.text) < 100:
            return "⚠️ The publisher is blocking automated previews. Use the link below to read."
            
        return article.text[:600] + "..."
    except Exception as e:
        return "❌ Preview failed. The site might be protected or require a subscription."

# 3. Language Localization Dictionary
lang_options = {
    "English": {
        "title": "🗞️ News Hub: Greece & Europe",
        "search_label": "🔍 Search topics",
        "placeholder": "e.g. Economy...",
        "greece_header": "🇬🇷 Greece",
        "europe_header": "🇪🇺 Europe",
        "time_label": "Athens Local Time",
        "posted": "Posted",
        "read_btn": "Read Preview",
        "close_btn": "Close",
        "gr_lang": "en-GR",
        "gr_gl": "GR"
    },
    "Ελληνικά": {
        "title": "🗞️ Ενημέρωση: Ελλάδα & Ευρώπη",
        "search_label": "🔍 Αναζήτηση θεμάτων",
        "placeholder": "π.χ. Οικονομία...",
        "greece_header": "🇬🇷 Ελλάδα",
        "europe_header": "🇪🇺 Ευρώπη (English)",
        "time_label": "Ώρα Αθήνας",
        "posted": "Δημοσιεύτηκε",
        "read_btn": "Προεπισκόπηση",
        "close_btn": "Κλείσιμο",
        "gr_lang": "el",
        "gr_gl": "GR"
    }
}

# 4. Sidebar Setup
st.sidebar.title("Settings / Ρυθμίσεις")
selected_lang = st.sidebar.selectbox("Language / Γλώσσα", ["English", "Ελληνικά"])
L = lang_options[selected_lang]

# 5. Timezone & Formatting
athens_tz = pytz.timezone('Europe/Athens')

def format_date_athens(struct_time):
    if not struct_time: return "Recently"
    dt_utc = datetime(*struct_time[:6], tzinfo=pytz.utc)
    dt_athens = dt_utc.astimezone(athens_tz)
    return dt_athens.strftime("%a, %d %b %H:%M")

# 6. Header & Search
current_time = datetime.now(athens_tz).strftime("%H:%M:%S")
st.title(L["title"])
st.caption(f"{L['time_label']}: {current_time}")

search_query = st.text_input(L["search_label"], placeholder=L["placeholder"])
safe_query = urllib.parse.quote_plus(search_query)

# 7. Fetch Data
sources = {
    "Greece": f"https://news.google.com/rss/search?q={safe_query}+Greece&hl={L['gr_lang']}&gl={L['gr_gl']}&ceid={L['gr_gl']}:{L['gr_lang']}",
    "Europe": f"https://news.google.com/rss/search?q={safe_query}+Europe&hl=en-150&gl=GR&ceid=GR:en"
}

feed_gr = feedparser.parse(sources["Greece"]).entries[:12]
feed_eu = feedparser.parse(sources["Europe"]).entries[:12]

st.markdown("---")
h_col1, h_col2 = st.columns(2)
h_col1.subheader(L["greece_header"])
h_col2.subheader(L["europe_header"])

# 8. The Grid Logic
for i, (gr, eu) in enumerate(zip_longest(feed_gr, feed_eu)):
    row_class = "even-row" if i % 2 == 0 else "odd-row"
    col1, col2 = st.columns(2)
    
    # GREECE COLUMN
    with col1:
        if gr:
            time_str = format_date_athens(gr.get('published_parsed'))
            st.markdown(f"""<div class='news-row {row_class}'>
                <a class='news-title' href='{gr.link}' target='_blank'>{gr.title}</a><br>
                <span class='timestamp'>🕒 {L['posted']}: {time_str}</span>
                </div>""", unsafe_allow_html=True)
            
            # Content Preview Expander
            with st.expander(L["read_btn"]):
                if st.button("Load Summary", key=f"gr_{i}"):
                    with st.spinner('Extracting...'):
                        text = get_article_preview(gr.link)
                        st.write(text)
                        st.markdown(f"[Source Link]({gr.link})")

    # EUROPE COLUMN
    with col2:
        if eu:
            time_str = format_date_athens(eu.get('published_parsed'))
            st.markdown(f"""<div class='news-row {row_class}'>
                <a class='news-title' href='{eu.link}' target='_blank'>{eu.title}</a><br>
                <span class='timestamp'>🕒 {L['posted']}: {time_str}</span>
                </div>""", unsafe_allow_html=True)
            
            # Content Preview Expander
            with st.expander(L["read_btn"]):
                if st.button("Load Summary", key=f"eu_{i}"):
                    with st.spinner('Extracting...'):
                        text = get_article_preview(eu.link)
                        st.write(text)
                        st.markdown(f"[Source Link]({eu.link})")

st.markdown("---")
st.caption("Powered by Google News RSS & Newspaper4k")