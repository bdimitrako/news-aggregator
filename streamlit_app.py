import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time

# 1. Page Config
st.set_page_config(layout="wide", page_title="News Hub", page_icon="🗞️")

# 2. Feedly Branding & Dark Theme CSS
FEEDLY_GREEN = "#2bb24c"
FEEDLY_GREY = "#30363d"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #fafafa; }}
    
    /* Header & Top Bar */
    .top-bar {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }}
    
    /* Feedly Typography: White titles, Green on Hover */
    .news-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: #ffffff !important;
        text-decoration: none !important;
        display: block;
        margin-bottom: 4px;
        line-height: 1.4;
    }}
    .news-title:hover {{ color: {FEEDLY_GREEN} !important; }}

    .metadata {{ font-size: 0.85rem; color: #8b949e; }}
    .source-site {{ font-weight: 600; color: #c9d1d9; margin-right: 10px; text-transform: lowercase; }}

    .section-header {{
        font-size: 0.95rem;
        font-weight: 800;
        color: #8b949e;
        border-bottom: 1px solid {FEEDLY_GREY};
        padding-bottom: 5px;
        margin-top: 20px;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    .feedly-row {{ padding: 12px 0; border-bottom: 1px solid {FEEDLY_GREY}; }}

    /* Custom Search Input Styling */
    div[data-testid="stTextInput"] input {{
        background-color: #161b22;
        border: 1px solid #30363d;
        color: white;
        border-radius: 4px;
    }}
    </style>
""", unsafe_allow_html=True)

# 3. Header: Clock, Search, and Toggle
athens_tz = pytz.timezone('Europe/Athens')
now_athens = datetime.now(athens_tz).strftime("%a, %d %b | %H:%M")

# Create a clean top layout
row1_col1, row1_col2, row1_col3 = st.columns([2, 2, 1])

with row1_col1:
    st.markdown(f"<h2 style='margin:0;'>🗞️ News Hub</h2>", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#8b949e; font-size:0.9rem;'>{now_athens}</span>", unsafe_allow_html=True)

with row1_col2:
    search_query = st.text_input("", placeholder="Search topics...", label_visibility="collapsed")

with row1_col3:
    # Custom Binary Toggle Button Logic
    if "lang" not in st.session_state:
        st.session_state.lang = "EN"
    
    # Render two small columns for the EN/GR switch
    sw1, sw2 = st.columns(2)
    with sw1:
        if st.button("EN", type="primary" if st.session_state.lang == "EN" else "secondary", use_container_width=True):
            st.session_state.lang = "EN"
            st.rerun()
    with sw2:
        if st.button("GR", type="primary" if st.session_state.lang == "GR" else "secondary", use_container_width=True):
            st.session_state.lang = "GR"
            st.rerun()

# 4. Data Logic
lang_key = st.session_state.lang
lang_map = {
    "EN": {"gr": "GR Greece", "eu": "EU Europe", "hl": "en-GR", "gl": "GR"},
    "GR": {"gr": "GR Ελλάδα", "eu": "EU Ευρώπη", "hl": "el", "gl": "GR"}
}
L = lang_map[lang_key]

@st.cache_data(ttl=600)
def get_news(query, hl, gl):
    q = urllib.parse.quote_plus(query)
    base_url = f"https://news.google.com/rss/search?q={q}"
    return feedparser.parse(f"{base_url}&hl={hl}&gl={gl}").entries[:15]

feed_gr = get_news(f"{search_query} Greece", L['hl'], L['gl'])
feed_eu = get_news(f"{search_query} Europe", "en-150", "GR")

# 5. The List View
def render_item(entry):
    parts = entry.title.rsplit(" - ", 1)
    title = parts[0]
    site = parts[1] if len(parts) > 1 else "news"
    
    if 'published_parsed' in entry:
        dt = datetime.fromtimestamp(time.mktime(entry.published_parsed))
        date_str = dt.strftime("%d %b, %H:%M")
    else:
        date_str = "now"

    st.markdown(f"""
        <div class="feedly-row">
            <a class="news-title" href="{entry.link}" target="_blank">{title}</a>
            <div class="metadata">
                <span class="source-site">{site}</span>
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