import streamlit as st
import feedparser
from datetime import datetime
import pytz

# 1. Set Page and Timezone
st.set_page_config(layout="wide", page_title="GR/EU News Hub")
greece_tz = pytz.timezone('Europe/Athens')
current_time = datetime.now(greece_tz).strftime("%H:%M:%S")

st.title("🗞️ News Dashboard: Greece & Europe")
st.caption(f"Greek Local Time: {current_time} (Athens)")

# 2. Define Feeds
sources = {
    "Greece": "https://news.google.com/rss/search?q=Greece+news&hl=en-GR&gl=GR",
    "Europe": "https://news.google.com/rss/search?q=Europe+news&hl=en-150&gl=GR"
}

# Fetch data
feed_gr = feedparser.parse(sources["Greece"]).entries[:10]
feed_eu = feedparser.parse(sources["Europe"]).entries[:10]

# 3. Create Header Row
h_col1, h_col2 = st.columns(2)
h_col1.header("🇬🇷 Greece")
h_col2.header("🇪🇺 Europe")
st.divider()

# 4. Grid Alignment (The "Row" Trick)
# We loop through both lists at the same time to force alignment
for gr_item, eu_item in zip(feed_gr, feed_eu):
    col1, col2 = st.columns(2)
    
    with col1:
        # Greece News
        st.markdown(f"**[{gr_item.title}]({gr_item.link})**")
        st.caption(f"Source: {gr_item.source.title if 'source' in gr_item else 'News'}")

    with col2:
        # Europe News
        st.markdown(f"**[{eu_item.title}]({eu_item.link})**")
        st.caption(f"Source: {eu_item.source.title if 'source' in eu_item else 'News'}")
    
    st.divider()