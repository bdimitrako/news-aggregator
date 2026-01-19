import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time

# 1. Page Config
st.set_page_config(layout="wide", page_title="News Hub", page_icon="🗞️")

FEEDLY_GREEN = "#2bb24c"
FEEDLY_GREY = "#30363d"

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
        line-height: 1.4;
    }}
    .news-title:hover {{ color: {FEEDLY_GREEN} !important; }}

    .metadata {{ font-size: 0.85rem; color: #8b949e; }}
    .source-site {{ font-weight: 600; color: #c9d1d9; margin-right: 10px; text-transform: lowercase; }}

    .section-header {{
        font-size: 0.9rem;
        font-weight: 800;
        color: #8b949e;
        border-bottom: 1px solid {FEEDLY_GREY};
        padding-bottom: 5px;
        margin-top: 20px;
        margin-bottom: 15px;
        text-transform: uppercase;
    }}

    .feedly-row {{ padding: 12px 0; border-bottom: 1px solid {FEEDLY_GREY}; }}

    /* FIX: Force 'Primary' buttons to be Feedly Green and remove red tint */
    button[data-testid="baseButton-primary"] {{
        background-color: {FEEDLY_GREEN} !important;
        color: white !important;
        border: none !important;
    }}
    
    /* Search Bar custom style */
    div[data-testid="stTextInput"] input {{
        background-color: #161b22;
        border: 1px solid #30363d;
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

# 2. Header & Clock
athens_tz = pytz.timezone('Europe/Athens')
now_athens = datetime.now(athens_tz).strftime("%a, %d %b | %H:%M")

head_col, search_col, toggle_col = st.columns([1.5, 2, 1.2])

with head_col:
    st.markdown(f"<h2 style='margin:0;'>🗞️ News Hub</h2>", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#8b949e; font-size:0.9rem;'>{now_athens}</span>", unsafe_allow_html=True)

with search_col:
    st.write("##")
    search_query = st.text_input("", placeholder="Search topics...", label_visibility="collapsed")

with toggle_col:
    st.write("##")
    if "lang" not in st.session_state:
        st.session_state.lang = "EN"
    
    # Binary Switch Logic
    c1, c2 = st.columns(2)
    with c1:
        # Fixed 'type' parameter
        if st.button("🇬🇧 EN", type="primary" if st.session_state.lang == "EN" else "secondary", use_container_width=True):
            st.session_state.lang = "EN"
            st.rerun()
    with c2:
        # Fixed 'type' parameter
        if st.button("🇬🇷 GR", type="primary" if st.session_state.lang == "GR" else "secondary", use_container_width=True):
            st.session_state.lang = "GR"
            st.rerun()

# 3. Data Loading
L = {
    "EN": {"gr": "GR Greece", "eu": "EU Europe", "hl": "en-GR", "gl": "GR"},
    "GR": {"gr": "GR Ελλάδα", "eu": "EU Ευρώπη", "hl": "el", "gl": "GR"}
}[st.session_state.lang]

@st.cache_data(ttl=600)
def get_news(q, hl, gl):
    safe_q = urllib.parse.quote_plus(q)
    return feedparser.parse(f"https://news.google.com/rss/search?q={safe_q}&hl={hl}&gl={gl}").entries[:15]

feed_gr = get_news(f"{search_query} Greece", L['hl'], L['gl'])
feed_eu = get_news(f"{search_query} Europe", "en-150", "GR")

# 4. Content Display
def render_item(entry):
    parts = entry.title.rsplit(" - ", 1)
    title, site = (parts[0], parts[1]) if len(parts) > 1 else (entry.title, "news")
    dt_str = datetime.fromtimestamp(time.mktime(entry.published_parsed)).strftime("%d %b, %H:%M") if 'published_parsed' in entry else "now"

    st.markdown(f"""
        <div class="feedly-row">
            <a class="news-title" href="{entry.link}" target="_blank">{title}</a>
            <div class="metadata">
                <span class="source-site">{site}</span> • {dt_str}
            </div>
        </div>
    """, unsafe_allow_html=True)

col_gr, col_eu = st.columns(2)
with col_gr:
    st.markdown(f"<div class='section-header'>{L['gr']}</div>", unsafe_allow_html=True)
    for item in feed_gr: render_item(item)
with col_eu:
    st.markdown(f"<div class='section-header'>{L['eu']}</div>", unsafe_allow_html=True)
    for item in feed_eu: render_item(item)