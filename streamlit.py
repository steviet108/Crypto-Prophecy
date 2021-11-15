import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv
from nomics import Nomics
import json
import plotly
import tweepy
import yfinance as yf

# Load .env environment variables
load_dotenv()

# Header for main and sidebar
st.title( "Crypto Prophet")
st.sidebar.title("Options")

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

# This code gives us the sidebar on streamlit for the different dashboards
option = st.sidebar.selectbox("Dashboards", ('Top 100 Cryptocurrencies by Market Cap', 'Coin Analysis', 'Google Trends', ' Tweet Counts', 'Charts'), 1)
#option_1 = st.sidebar.text_input("coin", value="{symbol}", max_chars=5)
# This is the Header for each page
st.header(option)

# This code gives us the Widget, for now its just an example but we can integrate into the Monte carlo simulation by nesting the code for Monte Carlo into this command.
num_days = st.sidebar.slider('Amount to Invest', 1, 100000, 10)

# This option gives users the ability to view the current top 100 cryptocurrencies
if option == 'Top 100 Cryptocurrencies by Market Cap':

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

# This option gives users the ability to view the current top 100 cryptocurrencies
if option == 'Coin Analysis':
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


# This is the Charts option on dashboard dropdown, and we can make it dynamic for each coin the api call gives us.
# Make this function dynamic 
if option == 'Charts':
    st.header("Coin Charts")
    #symbol = word[1:]
    st.write({})
    st.sidebar.text_input("coin", value='BTC', max_chars=5)

    st.image("https://charts2.finviz.com/chart.ashx?t=AAPL")


# This is the Google Trends option on dashboard dropdown, and we can make it dynamic for each coin the api call gives us.    
if option == 'Google Trends':
    st.header("Google Trends")
    #st.image(f"/Users/stephenthomas/Desktop/dashboard/Google_Trends.png")
    st.image(f"/Users/stephenthomas/Desktop/dashboard/Google_Trends.png")

# This is the code for the Twitter API call and the query to do a full search of archives. The API is working but I can't figure out how to parse the info we want.   
if option == 'Tweet Counts':
    st.header("Tweet Counts")
    tweepy_consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    tweepy_consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    tweepy_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    tweepy_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")


    tweepy_auth = tweepy.OAuthHandler("tweepy_consumer_key" , "tweepy_consumer_secret")
    tweepy_auth.set_access_token("tweepy_access_token", "tweepy_access_token_secret")
    api = tweepy.API(tweepy_auth)
    
    public_tweets = api.search_full_archive("production", "BTC")
    for tweet in public_tweets:
        if "#BTC" in tweet.text:
            words = tweet.text.split(' ')
            for word in words:
                if word.startswith('#') and word[1:].isalpha():
                    symbol = word[1:]
                    st.write(symbol)

                    st.write(tweet.text)

    
       
        
    
    
    