import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime
import pytz

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="News Hub", page_icon="🗞️")

# 2. Feedly Branding & Custom CSS
FEEDLY_GREEN = "#2bb24c"

st.markdown(f"""
    <style>
    /* Clean white background like Feedly */
    .stApp {{ background-color: #ffffff; color: #333; }}
    
    /* Header styling with Feedly Green underlines */
    .section-header {{
        font-size: 1.1rem;
        font-weight: 800;
        color: #1e1e1e;
        border-bottom: 2px solid {FEEDLY_GREEN};
        padding-bottom: 8px;
        margin-top: 20px;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* Feedly List Row */
    .feedly-row {{
        padding: 10px 0;
        border-bottom: 1px solid #eef0f2;
        transition: background 0.2s;
    }}
    .feedly-row:hover {{ background-color: #f9f9f9; }}

    /* Title: Bold, No Underline */
    .news-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: #222 !important;
        text-decoration: none !important;
        display: block;
        line-height: 1.4;
        margin-bottom: 4px;
    }}
    .news-title:hover {{ color: {FEEDLY_GREEN} !important; }}

    /* Metadata: Grey text, Site name on the left */
    .metadata {{
        font-size: 0.85rem;
        color: #888;
        display: flex;
        align-items: center;
    }}
    .source-site {{
        font-weight: 600;
        color: #555;
        margin-right: 10px;
        text-transform: lowercase;
    }}

    /* Styling the Toggle Switch to match Feedly colors */
    div[data-testid="stToggle"] > label > div[role="switch"][aria-checked="true"] {{
        background-color: {FEEDLY_GREEN} !important;
    }}

    /* Mobile: Ensure columns stack correctly */
    @media (max-width: 800px) {{
        [data-testid="column"] {{ width: 100% !important; flex: 1 1 100% !important; }}
    }}
    </style>
""", unsafe_allow_html=True)

# 3. Language Toggle & Header
header_col, toggle_col = st.columns([4, 1])

with header_col:
    st.markdown("<h1 style='margin:0; font-weight:900;'>News Hub</h1>", unsafe_allow_html=True)

with toggle_col:
    # Toggle switch with EN/GR label
    is_gr = st.toggle("EN / GR", value=False)
    lang_key = "Ελληνικά" if is_gr else "English"

# 4. Data Config
lang_map = {
    "English": {"gr": "GR Greece", "eu": "EU Europe", "hl": "en-GR", "gl": "GR"},
    "Ελληνικά": {"gr": "GR Ελλάδα", "eu": "EU Ευρώπη", "hl": "el", "gl": "GR"}
}
L = lang_map[lang_key]

# 5. Fetching (RSS)
sources = {
    "Greece": f"https://news.google.com/rss/search?q=Greece&hl={L['hl']}&gl={L['gl']}",
    "Europe": f"https://news.google.com/rss/search?q=Europe&hl=en-150&gl=GR"
}

feed_gr = feedparser.parse(sources["Greece"]).entries[:15]
feed_eu = feedparser.parse(sources["Europe"]).entries[:15]

# 6. Render the "Feedly" View
col1, col2 = st.columns(2)

def render_feedly_style(entry):
    if not entry: return
    # Split "Title - Site Name" usually provided by Google News
    title_parts = entry.title.rsplit(" - ", 1)
    title = title_parts[0]
    site = title_parts[1] if len(title_parts) > 1 else "news"
    
    # Simple timestamp extraction
    time_str = entry.published.split(' ')[4][:5] if 'published' in entry else "now"

    st.markdown(f"""
        <div class="feedly-row">
            <a class="news-title" href="{entry.link}" target="_blank">{title}</a>
            <div class="metadata">
                <span class="source-site">{site}</span>
                <span>/ {time_str}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col1:
    st.markdown(f"<div class='section-header'>{L['gr']}</div>", unsafe_allow_html=True)
    for entry in feed_gr:
        render_feedly_style(entry)

with col2:
    st.markdown(f"<div class='section-header'>{L['eu']}</div>", unsafe_allow_html=True)
    for entry in feed_eu:
        render_feedly_style(entry)