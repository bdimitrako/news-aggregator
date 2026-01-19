import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from itertools import zip_longest

# 1. Config & Enhanced Mobile Styling
st.set_page_config(layout="wide", page_title="News Hub", page_icon="🗞️")

st.markdown("""
    <style>
    /* Fix mobile padding */
    .block-container { 
        padding-top: 1.5rem; 
        padding-left: 1rem !important; 
        padding-right: 1rem !important; 
    }
    
    /* Better News Cards */
    .news-card { 
        padding: 18px; 
        border-radius: 12px; 
        margin-bottom: 15px; 
        border: 1px solid #30363d; 
        background-color: #161b22;
        display: flex;
        flex-direction: column;
    }
    
    /* Title Styling - Ensures no overflow */
    .news-title { 
        font-size: 1.15rem; 
        font-weight: 600; 
        text-decoration: none; 
        color: #58a6ff !important; 
        line-height: 1.4;
        word-wrap: break-word;
        margin-bottom: 8px;
    }
    
    .timestamp { 
        font-size: 0.85rem; 
        color: #8b949e; 
        font-family: -apple-system, BlinkMacSystemFont, sans-serif; 
    }

    /* FORCING STACK ON MOBILE */
    @media (max-width: 800px) {
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            padding: 0 !important;
            margin-bottom: 10px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 2. Language Options
lang_options = {
    "English": {
        "title": "🗞️ News Hub", 
        "greece": "🇬🇷 Greece", 
        "europe": "🇪🇺 Europe", 
        "posted": "Posted",
        "search": "🔍 Search topics...",
        "gr_lang": "en-GR", 
        "gr_gl": "GR"
    },
    "Ελληνικά": {
        "title": "🗞️ Ενημέρωση", 
        "greece": "🇬🇷 Ελλάδα", 
        "europe": "🇪🇺 Ευρώπη", 
        "posted": "Δημοσιεύτηκε",
        "search": "🔍 Αναζήτηση θεμάτων...",
        "gr_lang": "el", 
        "gr_gl": "GR"
    }
}

# 3. Sidebar & Time
st.sidebar.title("Settings")
selected_lang = st.sidebar.selectbox("Language / Γλώσσα", ["English", "Ελληνικά"])
L = lang_options[selected_lang]
athens_tz = pytz.timezone('Europe/Athens')

def format_date(struct_time):
    if not struct_time: return "Recently"
    dt = datetime(*struct_time[:6], tzinfo=pytz.utc).astimezone(athens_tz)
    return dt.strftime("%d %b, %H:%M")

# 4. Search & Fetch
st.title(L["title"])
search_query = st.text_input(L["search"], "")
safe_query = urllib.parse.quote_plus(search_query)

sources = {
    "Greece": f"https://news.google.com/rss/search?q={safe_query}+Greece&hl={L['gr_lang']}&gl={L['gr_gl']}",
    "Europe": f"https://news.google.com/rss/search?q={safe_query}+Europe&hl=en-150&gl=GR"
}

feed_gr = feedparser.parse(sources["Greece"]).entries[:12]
feed_eu = feedparser.parse(sources["Europe"]).entries[:12]

# 5. The Grid
col_left, col_right = st.columns(2)

def render_item(entry):
    if not entry: return
    time_str = format_date(entry.get('published_parsed'))
    # Using a clean div structure instead of expanders for a faster mobile feel
    st.markdown(f"""
        <div class="news-card">
            <a class="news-title" href="{entry.link}" target="_blank">{entry.title}</a>
            <div class="timestamp">🕒 {L['posted']}: {time_str}</div>
        </div>
    """, unsafe_allow_html=True)

with col_left:
    st.subheader(L["greece"])
    for item in feed_gr: render_item(item)

with col_right:
    st.subheader(L["europe"])
    for item in feed_eu: render_item(item)