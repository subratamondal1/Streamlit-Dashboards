# ---Import Libraries--- #
import streamlit as st
import requests
import json
import time
import numpy as np
import pandas as pd

# ---Page Config--- #
st.set_page_config(page_title="#Dashboards", layout="wide",
                   initial_sidebar_state="expanded")

# ---Sidebar---
st.sidebar.title("#Dashboards")
option = st.sidebar.selectbox(
    "**`Choose a Dashboard`**", ("countries", "polygon stock"))
# ---Read CSS--- #
with open("styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if option == "countries":
    class CountryData:
        def __init__(self):
            self.__by_country_url = "https://restcountries.com/v3.1/name/"
            self.__by_currency_url = "https://restcountries.com/v3.1/currency/"

        def get_country_data(self, country):
            response = requests.get(
                f"{self.__by_country_url}{country.lower()}")
            data = json.loads(response.text)

            # attribute data that will be returned
            commonName = data[0]["name"]["common"]
            officalName = data[0]["name"]["official"]
            capital = data[0]['capital'][0]
            currency = list(dict(data[0]['currencies']).keys())[0]
            currenyFullName = data[0]['currencies'][list(
                dict(data[0]['currencies']).keys())[0]]["name"]
            currencySymbol = data[0]['currencies'][list(
                dict(data[0]['currencies']).keys())[0]]["symbol"]
            region = data[0]['region']
            subRegion = data[0]['subregion']
            area = data[0]['area']
            population = data[0]['population']
            googleMap = data[0]['maps']['googleMaps']
            flagSvg = data[0]['flags']['svg']
            final_data = {"commonName": commonName,
                          "officalName": officalName,
                          "currency": currency,
                          "currenyFullName": currenyFullName,
                          "currencySymbol": currencySymbol,
                          "capital": capital,
                          "region": region,
                          "subRegion": subRegion,
                          "area": area,
                          "population": population,
                          "googleMap": googleMap,
                          "flagSvg": flagSvg}
            return final_data
    country_data = CountryData()

    with st.sidebar:
        country = st.text_input("**`by Country`**", "india")
        # capital = st.text_input("**`by Country`**", "delhi")

        response = requests.get(
            f"https://restcountries.com/v3.1/name/{country}").text
        data = json.loads(response)

    st.title(data[0]["name"]["official"])
    # st.write(country_data.get_country_data(country))
    country_df = pd.DataFrame(
        country_data.get_country_data(country), index=[0])

    # container 1
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(country_df["flagSvg"].values[0])
        with col2:
            st.metric(
                "Country", country_df["commonName"].values[0], country_df["officalName"].values[0])
        with col3:
            st.metric("Capital", country_df["capital"].values[0])

    # container 2
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Currency", f"{country_df['currency'].values[0]} ‣ {country_df['currencySymbol'].values[0]}",
                      country_df["currenyFullName"].values[0])
        with col2:
            st.metric(
                "Population", f"{round((country_df['population'].values[0] / 1000000))}M", "M ‣ Millions")
        with col3:
            st.metric(
                "Area", f"{round((country_df['area'].values[0])/1000)}K", "Square Kilometers")


# ---Polygon--- #
if option == "polygon stock":
    ticker = st.sidebar.text_input("**`Symbol`**", value="AAPL")

    class ApiCalls:
        """
        All the API calls are made through this class!!!
        """

        def __init__(self, ticker):
            self.__API_KEY = "3yOpyixTkLBex3xp0Sm6yeVtalxu4HLe"
            self.__ticker = ticker

        def get_symbol_data(self):
            # response of Symbols
            response_symbol = requests.get(
                f"https://api.polygon.io/v3/reference/tickers/{self.__ticker.upper()}?apiKey=3yOpyixTkLBex3xp0Sm6yeVtalxu4HLe")
            return json.loads(response_symbol.text)

        def get_daily_open_close(self):
            response_daily_open_close = requests.get(
                f"https://api.polygon.io/v1/open-close/{self.__ticker.upper()}/2023-01-09?adjusted=true&apiKey=3yOpyixTkLBex3xp0Sm6yeVtalxu4HLe")
            return json.loads(response_daily_open_close.text)

        def get_pandas_df(self):
            response = requests.get()

    # data
    data = ApiCalls(ticker)
    ticker_data = data.get_symbol_data()
    ticker_daily_open_close = data.get_daily_open_close()

    if ticker_data["status"] != "OK":
        st.info("Max api calls per min is 5, so wait for a bit and refresh")

    class CompanyDetails:
        """
        This class contains the details of the (company) symbols like
        - name
        - description
        - market cap.
        - listing date (IPO)
        """

        def __init__(self, data):
            self.__data = data
            self.__name = data["results"]["name"]
            self.__description = data["results"]["description"]
            self.__market_cap = int(data["results"]["market_cap"])
            self.__list_date = data["results"]["list_date"]

        def get_name(self):
            return self.__name

        def get_description(self):
            return self.__description

        def get_market_cap(self):
            return self.__market_cap / 1000000000  # in billion

        def get_list_date(self):
            return self.__list_date

    company_details = CompanyDetails(ticker_data)

    class DailyPrice:
        """
        This class contains daily open,high,close,price of the Symbol.
        It also contains the price of pre-market.
        """

        def __init__(self, data):
            self.__data = data
            self.__open = data["open"]
            self.__high = data["high"]
            self.__low = data["low"]
            self.__close = data["close"]
            self.__pre_market = data["preMarket"]

        def get_open_price(self):
            return round(float(self.__open), 2)

        def get_high_price(self):
            return round(float(self.__high), 2)

        def get_low_price(self):
            return round(float(self.__low), 2)

        def get_close_price(self):
            return round(float(self.__close), 2)

        def get_pre_market_price(self):
            return round(float(self.__pre_market), 2)

    daily_price = DailyPrice(ticker_daily_open_close)

    # open
    open = daily_price.get_open_price()
    # high
    high = daily_price.get_high_price()
    # low
    low = daily_price.get_low_price()
    # close
    close = daily_price.get_close_price()
    # pre_market
    pre_market = daily_price.get_pre_market_price()

    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Open", open,
                      f"{round(((open-pre_market)/pre_market)*100,2)} %")

        with col2:
            st.metric("High", high, f"{round(((high-low)/low)*100, 2)} %")

        with col3:
            st.metric("Low", low, f"{round(((low - open)/open)*100, 2)} %")

        with col4:
            st.metric("Close", close, f"{round(((close-open)/open)*100, 2)} %")

        with st.container():
            with st.expander(company_details.get_name(), expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    # ---LOGO--- #
                    logo = ticker_data["results"]["branding"]["logo_url"] + \
                        "?apiKey=3yOpyixTkLBex3xp0Sm6yeVtalxu4HLe"
                    st.image(logo, width=100)

                with col2:
                    st.metric("Market Cap.", round(
                        company_details.get_market_cap(), 2), "Billion $")

                with col3:
                    st.metric("IPO", company_details.get_list_date())

                st.write(company_details.get_description())


if option == "charts":
    st.title(option)
if option == "patterns":
    st.title(option)
