import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import json
import plotly
import tweepy
load_dotenv()

# Header for main and sidebar
st.title( "Crypto Prophet")
st.sidebar.title("Options")

# This code gives us the sidebar on streamlit for the different dashboards
option = st.sidebar.selectbox("Dashboards", ( 'Google Trends', 'Coin Analysis', ' Tweet Counts', 'Charts'), 2)
#option_1 = st.sidebar.text_input("coin", value="{symbol}", max_chars=5)
# This is the Header for each page
st.header(option)

# This code gives us the Widget, for now its just an example but we can integrate into the Monte carlo simulation by nesting the code for Monte Carlo into this command.
num_days = st.sidebar.slider('Amount to Invest', 1, 100000, 10)




if option == 'Coin Analysis':
    st.header("Coin Analysis")
    
    symbol = st.sidebar.text_input("coin", value='BTC', max_chars=5)

    #r = requests.get(f"URL{symbol}")










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
    tweepy_auth = tweepy.OAuthHandler("LSz4FuLR5xdgNwiUtQXvOimOW" , "ni7nB11naP8DL52QHxW7Bd7X291dZtj2gaNLJ5fi1WBgyYDFLI")
    tweepy_auth.set_access_token("1365097854142849024-2llscaHopykWCU0xNf13kbK5Ic4lRE", "CdEfqzQvjF47AhhlolvEImeoRFvRtCXRhvEa7858RjlAI")
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
    