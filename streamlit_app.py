import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
import collections
import re

# 1. Page Configuration & Custom CSS
st.set_page_config(layout="wide", page_title="News Hub", page_icon="🗞️")

FEEDLY_GREEN = "#2bb24c"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #fafafa; }}
    
    /* Feedly Headlines */
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

    /* Compact scrollable Tag Styling */
    div[data-testid="column"] {{ min-width: 0px !important; }}
    
    .stButton > button {{
        background-color: transparent !important;
        border: 1px solid #30363d !important;
        color: #8b949e !important;
        padding: 2px 10px !important;
        border-radius: 15px !important;
        height: 26px !important;
        font-size: 0.75rem !important;
        white-space: nowrap !important;
    }}
    .stButton > button:hover {{
        border-color: {FEEDLY_GREEN} !important;
        color: {FEEDLY_GREEN} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 2. Logic: State & Time
if "query" not in st.session_state:
    st.session_state.query = ""
if "lang" not in st.session_state:
    st.session_state.lang = "EN"

athens_tz = pytz.timezone('Europe/Athens')
now = datetime.now(athens_tz)

# Top Navigation Bar
c1, c2, c3 = st.columns([1.5, 2, 1.2])

with c1:
    st.markdown(f"<h2 style='margin:0;'>🗞️ News Hub</h2>", unsafe_allow_html=True)
    st.markdown(f"<span style='color:#8b949e;'>{now.strftime('%a, %d %b | %H:%M')}</span>", unsafe_allow_html=True)

with c2:
    st.write("##")
    search_input = st.text_input("", value=st.session_state.query, placeholder="Search topics...", label_visibility="collapsed")
    st.session_state.query = search_input

with c3:
    st.write("##")
    l1, l2 = st.columns(2)
    with l1:
        if st.button("EN", type="primary" if st.session_state.lang == "EN" else "secondary", use_container_width=True):
            st.session_state.lang = "EN"
            st.rerun()
    with l2:
        if st.button("GR", type="primary" if st.session_state.lang == "GR" else "secondary", use_container_width=True):
            st.session_state.lang = "GR"
            st.rerun()

# 3. Data Fetching & Dynamic Tag Extraction
L = {"EN": {"hl": "en-GR", "gl": "GR"}, "GR": {"hl": "el", "gl": "GR"}}[st.session_state.lang]

@st.cache_data(ttl=600)
def get_sorted_news(q, hl, gl):
    safe_q = urllib.parse.quote(q)
    url = f"https://news.google.com/rss/search?q={safe_q}&hl={hl}&gl={gl}&ceid={gl}:{hl}"
    feed = feedparser.parse(url)
    entries = feed.entries
    # Sort latest first
    entries.sort(key=lambda x: x.get('published_parsed', 0), reverse=True)
    return entries[:20]

def extract_hashtags(entries, num=8):
    words = []
    stop = {'the', 'and', 'for', 'with', 'from', 'says', 'after', 'news', 'greece', 'europe', 'greeks', 'will'}
    for e in entries:
        clean = re.sub(r'[^\w\s]', '', e.title.lower())
        words.extend([w for w in clean.split() if len(w) > 4 and w not in stop])
    return [w[0].capitalize() for w in collections.Counter(words).most_common(num)]

# Initial fetch to get tags
f_gr = get_sorted_news(f"{st.session_state.query} Greece", L['hl'], L['gl'])
f_eu = get_sorted_news(f"{st.session_state.query} Europe", "en-150", "GR")

# 4. Hashtag Row (Dynamic)
tags = extract_hashtags(f_gr + f_eu)
if tags:
    tag_cols = st.columns(len(tags))
    for i, tag in enumerate(tags):
        with tag_cols[i]:
            if st.button(f"#{tag.lower()}", key=f"t_{tag}"):
                st.session_state.query = tag
                st.rerun()

# 5. Rendering
def render_news(entry):
    parts = entry.title.rsplit(" - ", 1)
    title = parts[0]
    site = parts[1] if len(parts) > 1 else "news"
    date_str = datetime.fromtimestamp(time.mktime(entry.published_parsed)).strftime("%d %b, %H:%M") if 'published_parsed' in entry else ""
    
    st.markdown(f"""
        <div class="feedly-row">
            <a class="news-title" href="{entry.link}" target="_blank">{title}</a>
            <div class="metadata"><b>{site}</b> • {date_str}</div>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"<div class='section-header'>{'GR Ελλάδα' if st.session_state.lang == 'GR' else 'GR Greece'}</div>", unsafe_allow_html=True)
    for e in f_gr: render_news(e)

with col_right:
    st.markdown(f"<div class='section-header'>{'EU Ευρώπη' if st.session_state.lang == 'GR' else 'EU Europe'}</div>", unsafe_allow_html=True)
    for e in f_eu: render_news(e)