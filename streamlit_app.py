import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time

# 1. Page Config
st.set_page_config(layout="wide", page_title="News Hub")

FEEDLY_GREEN = "#2bb24c"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #fafafa; }}
    
    .news-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: #ffffff !important;
        text-decoration: none !important;
        display: block;
        margin-bottom: 4px;
    }}
    .news-title:hover {{ color: {FEEDLY_GREEN} !important; }}
    .metadata {{ font-size: 0.85rem; color: #8b949e; }}
    .feedly-row {{ padding: 12px 0; border-bottom: 1px solid #30363d; }}
    .section-header {{
        font-size: 0.9rem;
        font-weight: 800;
        color: #8b949e;
        border-bottom: 1px solid #30363d;
        padding-bottom: 5px;
        margin-bottom: 15px;
        text-transform: uppercase;
    }}
    /* Style for hashtag buttons to look like labels */
    div[data-testid="stHorizontalBlock"] button {{
        background-color: transparent !important;
        border: 1px solid #30363d !important;
        color: #8b949e !important;
        padding: 2px 8px !important;
        height: auto !important;
        font-size: 0.8rem !important;
    }}
    div[data-testid="stHorizontalBlock"] button:hover {{
        border-color: {FEEDLY_GREEN} !important;
        color: {FEEDLY_GREEN} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 2. State & Header
if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "query" not in st.session_state:
    st.session_state.query = ""

athens_tz = pytz.timezone('Europe/Athens')
now = datetime.now(athens_tz)

c1, c2, c3 = st.columns([1.5, 2, 1.2])

with c1:
    st.markdown(f"<h2 style='margin:0;'>🗞️ News Hub</h2>", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#8b949e;'>{now.strftime('%a, %d %b | %H:%M')}</span>", unsafe_allow_html=True)

with c2:
    st.write("##")
    # Link search input to session state
    search_input = st.text_input("", value=st.session_state.query, placeholder="Search topics...", label_visibility="collapsed")
    st.session_state.query = search_input

with c3:
    st.write("##")
    l_col1, l_col2 = st.columns(2)
    with l_col1:
        if st.button("EN", type="primary" if st.session_state.lang == "EN" else "secondary", use_container_width=True):
            st.session_state.lang = "EN"
            st.rerun()
    with l_col2:
        if st.button("GR", type="primary" if st.session_state.lang == "GR" else "secondary", use_container_width=True):
            st.session_state.lang = "GR"
            st.rerun()

# --- 2.5 Hashtag Row ---
hashtags = ["Politics", "Economy", "Tech", "Tourism", "Sports", "Energy", "Climate", "Health", "Ukraine", "Israel"]
tag_cols = st.columns(10)
for i, tag in enumerate(hashtags):
    with tag_cols[i]:
        if st.button(f"#{tag.lower()}", key=f"tag_{tag}"):
            st.session_state.query = tag
            st.rerun()

# 3. Data Fetching & Sorting Logic
L = {"EN": {"hl": "en-GR", "gl": "GR"}, "GR": {"hl": "el", "gl": "GR"}}[st.session_state.lang]

@st.cache_data(ttl=600)
def get_sorted_news(q, hl, gl):
    url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl={hl}&gl={gl}&ceid={gl}:{hl}"
    feed = feedparser.parse(url)
    entries = feed.entries
    entries.sort(key=lambda x: x.get('published_parsed', 0), reverse=True)
    return entries[:20]

# Use st.session_state.query for fetching
f_gr = get_sorted_news(f"{st.session_state.query} Greece", L['hl'], L['gl'])
f_eu = get_sorted_news(f"{st.session_state.query} Europe", "en-150", "GR")

# 4. Content Rendering
def render(entry):
    parts = entry.title.rsplit(" - ", 1)
    title = parts[0]
    site = parts[1] if len(parts) > 1 else "news"
    
    if 'published_parsed' in entry:
        dt = datetime.fromtimestamp(time.mktime(entry.published_parsed))
        date_str = dt.strftime("%d %b, %H:%M")
    else:
        date_str = ""
    
    st.markdown(f"""
        <div class="feedly-row">
            <a class="news-title" href="{entry.link}" target="_blank">{title}</a>
            <div class="metadata"><b>{site}</b> • {date_str}</div>
        </div>
    """, unsafe_allow_html=True)

col_gr, col_eu = st.columns(2)
with col_gr:
    st.markdown("<div class='section-header'>GR Greece</div>", unsafe_allow_html=True)
    for e in f_gr: render(e)
with col_eu:
    st.markdown("<div class='section-header'>EU Europe</div>", unsafe_allow_html=True)
    for e in f_eu: render(e)