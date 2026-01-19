import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from itertools import zip_longest

# 1. Config & Styling
st.set_page_config(layout="wide", page_title="News Hub")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .news-row { padding: 12px; border-radius: 8px; margin-bottom: 8px; min-height: 110px; }
    .even-row { background-color: #161b22; border: 1px solid #30363d; }
    .odd-row { background-color: #0d1117; }
    .timestamp { font-size: 0.8rem; color: #8b949e; font-family: monospace; }
    .news-title { font-size: 1.05rem; font-weight: 600; text-decoration: none; color: #58a6ff !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Language Localization Dictionary
lang_options = {
    "English": {
        "title": "🗞️ News Hub: Greece & Europe",
        "search_label": "🔍 Search topics",
        "placeholder": "e.g. Economy...",
        "greece_header": "🇬🇷 Greece",
        "europe_header": "🇪🇺 Europe",
        "time_label": "Athens Local Time",
        "posted": "Posted",
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
        "gr_lang": "el",
        "gr_gl": "GR"
    }
}

# 3. Sidebar Setup
st.sidebar.title("Settings / Ρυθμίσεις")
selected_lang = st.sidebar.selectbox("Language / Γλώσσα", ["English", "Ελληνικά"])
L = lang_options[selected_lang]

# 4. Timezone & Formatting
athens_tz = pytz.timezone('Europe/Athens')

def format_date_athens(struct_time):
    if not struct_time: return "Recently"
    dt_utc = datetime(*struct_time[:6], tzinfo=pytz.utc)
    dt_athens = dt_utc.astimezone(athens_tz)
    return dt_athens.strftime("%a, %d %b %Y %H:%M")

# 5. Header & Search
current_time = datetime.now(athens_tz).strftime("%H:%M:%S")
st.title(L["title"])
st.caption(f"{L['time_label']}: {current_time}")

search_query = st.text_input(L["search_label"], placeholder=L["placeholder"])
safe_query = urllib.parse.quote_plus(search_query)

# 6. Fetch Data
# Note: Europe stays en-150 (English/Europe) while Greece follows the toggle
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

# 7. The Grid
for i, (gr, eu) in enumerate(zip_longest(feed_gr, feed_eu)):
    row_class = "even-row" if i % 2 == 0 else "odd-row"
    col1, col2 = st.columns(2)
    
    with col1:
        if gr:
            time_str = format_date_athens(gr.get('published_parsed'))
            st.markdown(f"""<div class='news-row {row_class}'>
                <a class='news-title' href='{gr.link}' target='_blank'>{gr.title}</a><br>
                <span class='timestamp'>🕒 {L['posted']}: {time_str}</span>
                </div>""", unsafe_allow_html=True)

    with col2:
        if eu:
            time_str = format_date_athens(eu.get('published_parsed'))
            st.markdown(f"""<div class='news-row {row_class}'>
                <a class='news-title' href='{eu.link}' target='_blank'>{eu.title}</a><br>
                <span class='timestamp'>🕒 {L['posted']}: {time_str}</span>
                </div>""", unsafe_allow_html=True)