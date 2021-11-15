# Import the required libraries and dependencies
import pytest
from nomics import Nomics
import pandas as pd
import os
from dotenv import load_dotenv
import requests
import json
import urllib.request
import streamlit as st
from st_aggrid import AgGrid

# Load .env environment variables
load_dotenv()

# Title of Dataframe
st.subheader('Top 100 Cryptocurrencies by Market Cap')

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

    # Rename column labels
    columns=['Rank', 'Logo', 'Symbol', 'Currency', 'Price (USD)', 'Price Date', 'Market Cap']
    top_cryptos_df.columns=columns

    # Set rank as index
    top_cryptos_df.set_index('Rank', inplace=True)

    # Convert to Price and Market Cap to currency format
    pd.options.display.float_format = '${:,.2f}'.format

    # Convert text data type to numerical data type
    top_cryptos_df['Market Cap'] = top_cryptos_df['Market Cap'].astype('float64')


    # Convert Timestamp to date only
    top_cryptos_df['Price Date']=pd.to_datetime(top_cryptos_df['Price Date']).dt.date

    # Convert your links to html tags 
    def path_to_image_html(Logo):
        return '<img src="'+ Logo +'" width=30 >'
        
    # Display image in dataframe
    top_cryptos_df.Logo = path_to_image_html(top_cryptos_df.Logo)
    st.write(top_cryptos_df.to_html(escape=False), unsafe_allow_html=True)


