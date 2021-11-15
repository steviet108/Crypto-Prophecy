import pytest
from nomics import Nomics
import pandas as pd
import os
from dotenv import load_dotenv
import requests
import json
import urllib.request
import streamlit as st
import yfinance as yf

# Load .env environment variables
load_dotenv()

# Title of Dataframe
st.title('Cryptocurrency Comparison Dashboard')

# Get nomics api key
nomics_api_key = os.getenv("NOMICS_API_KEY")
nomics_url = "https://api.nomics.com/v1/prices?key=" + nomics_api_key
nomics_currency_url = ("https://api.nomics.com/v1/currencies/ticker?key=" + nomics_api_key + "&interval=1d,30d&per-page=100&page=1")

# Read API in json
nomics_df = pd.read_json(nomics_currency_url)

# Create an empty DataFrame for top cryptocurrencies
top_cryptos_df = pd.DataFrame()

# Get rank, crytocurrency, price, price_date, market cap
top_cryptos_df = nomics_df[['rank', 'logo_url', 'currency', 'name', 'price', 'price_date', 'market_cap']]

# Pulls list of cryptocurrencies from Alpaca
coin = top_cryptos_df['currency'] + "-USD"

# Creates a dropdown list of cryptocurrencies based on top 100 list
dropdown = st.multiselect("Select coin(s) to analyze", coin)

# Create start date for analysis
start = st.date_input('Start', value = pd.to_datetime('today'))

# Create end date for analysis
end = st.date_input('End', value = pd.to_datetime('today'))

if len(dropdown) > 0:
    comparison_df = yf.download(dropdown,start,end)['Adj Close']
    st.line_chart(comparison_df)

