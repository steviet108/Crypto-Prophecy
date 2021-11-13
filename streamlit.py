import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import json

# Title of App
st.title( "Crypto Prophet")

# This code gives us the sidebar on streamlit for the different dashboards
option = st.sidebar.selectbox("Dashboards?", ( 'Google Trends', 'Coin Analysis', 'Charts'), 2)

st.header(option)

# This code gives us the "Coin" type-in tab, and we can nest analysis into the sidebar option
symbol = st.sidebar.text_input("coin", value='BTC', max_chars=5)
# This code gives us the Widget, for now its just an example but we can integrate into the Monte carlo simulation by nesting the code for Monte Carlo into this command.
num_days = st.sidebar.slider('Amount to Invest', 1, 100000, 10)

# This is the Charts option on dashboard dropdown, and we can make it dynamic for each coin the api call gives us.
if option == 'Charts':
    st.header("Coin Charts")
    st.image("https://finviz.com/crypto_charts.ashx?t=BTCUSD")


# This is the Google Trends option on dashboard dropdown, and we can make it dynamic for each coin the api call gives us.    
if option == 'Google Trends':
    st.header("Google Trends")
    st.image(f"https://trends.google.com/trends/explore?date=2012-01-01%202021-11-13&q=bitcoin")

# This is the code for the Twitter API call and the query to do a full search of archives. The API is working but I can't figure out how to parse the info we want.   
if option == 'Tweet Counts':
    st.header("Tweet Counts")
    tweepy_auth = tweepy.OAuthHandler("TWITTER_CONSUMER_KEY" , "TWITTER_CONSUMER_SECRET")
    tweepy_auth.set_access_token("TWITTER_ACCESS_TOKEN", "TWITTER_ACCESS_TOKEN_SECRET")
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

    
       
        
    
    #st.write(data)
    