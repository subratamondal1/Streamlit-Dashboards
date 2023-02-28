# ---Import Libraries--- #
import streamlit as st
import requests
import json

# # Title
# st.title("Title")

# # Header
# st.header("Header")

# # Subheader
# st.subheader("Subheader")

# # write
# st.write("write")

# ---Sidebar---
st.sidebar.title("#Dashboards")
option = st.sidebar.selectbox("**`Choose a Dashboard`**", ("twitter",
                                                           "wallstreetbets", "polygon", "charts", "patterns"))

if option == "twitter":
    st.title(option)
if option == "wallstreetbets":
    st.title(option)
# ---Polygon--- #
if option == "polygon":
    # API KEY
    API_KEY = "3yOpyixTkLBex3xp0Sm6yeVtalxu4HLe"
    # symbol - Ticker V3
    symbol = st.sidebar.text_input("**`Symbol`**", value="AAPL")

    # ---RESPONSE---
    # response of Symbols
    response_symbol = requests.get(
        f"https://api.polygon.io/v3/reference/tickers/{symbol}?apiKey=3yOpyixTkLBex3xp0Sm6yeVtalxu4HLe")
    response_daily_open_close = requests.get(
        f"https://api.polygon.io/v1/open-close/{symbol}/2023-01-09?adjusted=true&apiKey=3yOpyixTkLBex3xp0Sm6yeVtalxu4HLe")

    # ---DATA--- #
    # Symbol data
    data_symbol = json.loads(response_symbol.text)
    data_symbol

    # Daily Open/Close data
    data_daily_open_close = json.loads(response_daily_open_close.text)
    data_daily_open_close

    # open
    open = data_daily_open_close["open"]
    # high
    high = data_daily_open_close["high"]
    # low
    low = data_daily_open_close["low"]
    # close
    close = data_daily_open_close["close"]
    # preMarket
    preMarket = data_daily_open_close["preMarket"]

    # ---LOGO--- #
    logo = data_symbol["results"]["branding"]["logo_url"] + \
        "?apiKey=3yOpyixTkLBex3xp0Sm6yeVtalxu4HLe"
    st.image(logo, width=40)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Open", open,
                  f"{round(((open-preMarket)/preMarket)*100,2)} %")

    with col2:
        st.metric("High", high, round(high-low, 2))

    with col3:
        st.metric("Low", low, round(low - open, 2))

    with col4:
        st.metric("Close", close, round(close-open, 2))


if option == "charts":
    st.title(option)
if option == "patterns":
    st.title(option)
