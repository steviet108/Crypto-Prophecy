# Import the required libraries and dependencies
import pytest
from nomics import Nomics
import pandas as pd
import os
from dotenv import load_dotenv
import requests
import json
import urllib.request
from PIL import Image
from IPython.display import Image, HTML
import streamlit as st
from st_aggrid import AgGrid

# Load .env environment variables
load_dotenv()

st.header("Top 100 Cryptocurrencies by Market Cap")

# Get nomics api key
nomics_api_key = os.getenv("NOMICS_API_KEY")
nomics_url = "https://api.nomics.com/v1/prices?key=" + nomics_api_key
nomics_currency_url = ("https://api.nomics.com/v1/currencies/ticker?key=" + nomics_api_key + "&interval=1d,30d&per-page=100&page=1")

# Read API in json
nomics_df = pd.read_json(nomics_currency_url)

# Create an empty DataFrame for top cryptocurrencies
top_cryptos_df = pd.DataFrame()

# Get rank, crytocurrency, price, 1d change, market cat, volume
top_cryptos_df = nomics_df[['rank', 'logo_url', 'currency', 'name', 'price', 'price_date', 'market_cap']]
# top_cryptos_df.set_index('rank', inplace=True)

# convert your links to html tags 
def path_to_image_html(logo_url):
    return '<img src="'+ logo_url +'" width=50 >'

# Display image in dataframe
top_cryptos_df.logo_url = path_to_image_html(top_cryptos_df.logo_url)
st.write(top_cryptos_df.to_html(escape=False), unsafe_allow_html=True)

# Index by rank

# Print top cryptos
# AgGrid(top_cryptos_df, height=2850, fit_columns_on_grid_load=True)