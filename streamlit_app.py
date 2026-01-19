import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time

# 1. Config & Theme Restoration
st.set_page_config(layout="wide", page_title="News Hub", page_icon="🗞️")

# Custom CSS for Dark Mode Feedly Style
FEEDLY_GREEN = "#2bb24c"
st.markdown(f"""
    <style>
    /* Restore Dark Background */
    .stApp {{ background-color: #0e1117; color: #fafafa; }}
    
    /* Section Headers */
    .section-header {{
        font-size: 1.1rem;
        font-weight: 800;
        color: #ffffff;
        border-bottom: 2px solid {FEEDLY_GREEN};
        padding-bottom: 8px;
        margin-top: 10px;
        margin-bottom: 15px;
        text-transform: uppercase;
    }}

    /* Feedly List Item */
    .feedly-row {{
        padding: 12px 0;
        border-bottom: 1px solid #30363d;
    }}
    
    .news-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: #58a6ff !important; /* GitHub/Feedly Blue-ish Dark Mode Link */
        text-decoration: none !important;
        display: block;
        margin-bottom: 4px;
    }}
    .news-title:hover {{ color: {FEEDLY_GREEN} !important; }}

    .metadata {{
        font-size: 0.85rem;
        color: #8b949e;
    }}
    .source-site {{
        font-weight: 600;
        color: #c9d1d9;
        margin-right: 10px;
    }}

    /* Custom Toggle Switch Color */
    div[data-testid="stToggle"] > label > div[role="switch"][aria-checked="true"] {{
        background-color: {FEEDLY_GREEN} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 2. Top Header with Clock & Toggle
athens_tz = pytz.timezone('Europe/Athens')
now_athens = datetime.now(athens_tz).strftime("%A, %d %b %Y | %H:%M")

head_col1, head_col2 = st.columns([3, 1])
with head_col1:
    st.markdown(f"<h1 style='margin:0;'>🗞️ News Hub</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#8b949e; margin-bottom:20px;'>📍 Athens: {now_athens}</p>", unsafe_allow_html=True)

with head_col2:
    st.write("") # Padding
    is_gr = st.toggle("EN / GR", value=False)
    selected_lang = "Ελληνικά" if is_gr else "English"

# 3. Language Logic
lang_map = {
    "English": {"gr": "GR Greece", "eu": "EU Europe", "hl": "en-GR", "gl": "GR"},
    "Ελληνικά": {"gr": "GR Ελλάδα", "eu": "EU Ευρώπη", "hl": "el", "gl": "GR"}
}
L = lang_map[selected_lang]

# 4. Data Fetching
@st.cache_data(ttl=600)
def fetch_news(url):
    return feedparser.parse(url).entries[:15]

sources = {
    "Greece": f"https://news.google.com/rss/search?q=Greece&hl={L['hl']}&gl={L['gl']}",
    "Europe": f"https://news.google.com/rss/search?q=Europe&hl=en-150&gl=GR"
}

feed_gr = fetch_news(sources["Greece"])
feed_eu = fetch_news(sources["Europe"])

# 5. Rendering the List
def render_item(entry):
    # Parse title and source
    parts = entry.title.rsplit(" - ", 1)
    title = parts[0]
    source = parts[1] if len(parts) > 1 else "news"
    
    # Parse date correctly
    if 'published_parsed' in entry:
        dt = datetime.fromtimestamp(time.mktime(entry.published_parsed))
        date_str = dt.strftime("%d %b, %H:%M")
    else:
        date_str = "Recently"

    st.markdown(f"""
        <div class="feedly-row">
            <a class="news-title" href="{entry.link}" target="_blank">{title}</a>
            <div class="metadata">
                <span class="source-site">{source}</span>
                <span>• {date_str}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"<div class='section-header'>{L['gr']}</div>", unsafe_allow_html=True)
    for item in feed_gr: render_item(item)

with col_right:
    st.markdown(f"<div class='section-header'>{L['eu']}</div>", unsafe_allow_html=True)
    for item in feed_eu: render_item(item)