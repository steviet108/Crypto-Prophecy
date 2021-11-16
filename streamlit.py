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
option = st.sidebar.selectbox("Dashboards", ('Top 100 Cryptocurrencies by Market Cap', 'Coin Analysis', 'Google Trends', ' Tweet Counts', 'Cycle Analysis'), 1)
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
    st.sidebar.text_input("coin", value='BTC', max_chars=5)
    st.image("https://charts2.finviz.com/chart.ashx?t=AAPL")

# This is the Cycle Analysis option on dashboard dropdown.
if option == 'Cycle Analysis':
    #st.header("Cycle Analysis")
    # path to static image cycle_analysis in the working folder.
    st.image(f"/Users/stephenthomas/Desktop/git_dashboard/Crypto-Prophecy/images/cycle_analysis.png")
    
    # Markdown: analysis of bitcoin cycle
    """
    ### Summary of BTC Market Cycle Analysis
    This Analysis of the Bitcoin Cycles is meant to help answer 2 questions.
    
    1 - When will Bitcoin top out this cycle?
    
    2 - What will the price be at the top of this cycle?
    
    Analysis of the market cycles is an attempt to shed light on these two questions, and give investors an edge in this market.
    Cycles are measured from the start to the weekly low after the previous macro high and we have the Bitcoin chart from July 2010 to present day, on a logarithmic growth curve.
    The logarithmic growth curve is described as something that first exhibits explosive growth followed by an increasing taper until it reaches a plateau. I find it 
    interesting that not only is this trend identified in nature but that bitcoins growth has followed it very closely since its beginning. 
    We are interested in trying to use past data to estimate the next macro high. 
    
    Cycle #1 Topped in June of 2011 with a closing price of around 18$ and then went on to crash down to around 2.15$ marking the end of cycle #1 and the
    begining of cycle #2. Cycle #1 was around 322 days and we saw a 37,750% increase in price. 
    
    Cycle #2 Rallied from 2.15$ to 1015$ in Dec. 2013, which was a 45,500% percent increase and then went on to crash down to around 210$ in Jan of 2015
    marking the end of cycle #2. Cycle #2 was 750 days long and approximately 2.3x longer than cycle #1 or 130% Longer. 
    
    Cycle #3 Started in Dec of 2018, 1 year after the previous cycle high, and rallied to around 20k$ per Bitcoin. This was a 9,000% percent increase and from the 
    beginning of cycle #3 to the cycle high, it was 1070 days, 1.4x longer or 43% longer. 
    
    At this point we have 3 cycles and one could say we have a trend. It is also clear that the cycles are getting longer but the rate that they are getting longer
    is shortening quite quickly. Cycle #1 was 322 days from bottom to top, cycle #2 from bottom to top was 750 days or 130% longer than previous cycle, cycle #3 was 
    1070 days from bottom to top or 43% longer than previous cycle, so what will cycle #4 look like?
    
    So what can we learn from this trend that will help us use statistics and data to estimate when will this cycle #4 will end?
    
    What will the price of BTC be?

    We know that the cycles are getting longer at a slower speed and if cycle #3 was 1070 days and 43% longer than the previous cycle than based on the data we can assume 
    cycle #4 will be longer than #3 at a reduced rate of lengthing. If we cut cycle #3's rate of lengthing in half and applied 20% to cycle #4's length we get about 200 days or cycle #4
    being 200 days longer than cycle #3. It is interesting to not that currently as of mid November 2021, cycle #4 is as long as cycle #3, around 1070 days. So add 20% to where we are today
    and that puts us right around mid May, 2022. If we did the same thing but applied 10% of cycle #3 rate of lengthing we get around March 1 2022. So lets agree for the 
    purpose of this exercise that cycle #4 will top somewhere in between March 1, 2022 and May 15, 2022.

    Ok, we have a rough idea of when Bitcoin will top, now lets look at some potential prices based on those dates. We know based on the bitcoin Logarithmic curve chart
    that Bitcoin tops when its touched the upper end of the red zone. This is seen in the last 3 cycles. #1 closed a weekly candle around 18$, #2 closed around 1k$ and
    #3 closed around 20k$. So if we extrapolate our historical data to the dates of when this cycle #4 can potentially top, we are given some potential targets.The first being a  weekly candle 
    closing around 150k$ in the beginning of March, and second a weekly candle closing in the middle of May around 175k$. As Mark Twain put it "History does'nt repeat but it does rhyme".
    """

# This is the Google Trends option on dashboard dropdown, and we can make it dynamic for each coin the api call gives us.    
if option == 'Google Trends':
    # Markdown: Explanation of how to read the folowing Google Trends charts.
    """Numbers on the Y-axis represent search interest relative to the highest point on the chart for the given region and time.
    A value of 100 is the peak popularity for the term. A value of 50 means that the term is half as popular. 
    A score of 0 means there was not enough data for this term."""
    # Google Trends chart.
    st.image(f"/Users/stephenthomas/Desktop/git_dashboard/Crypto-Prophecy/images/Google_Trends.png", caption="Worldwide Interest in Bitcoin 2012 - 2021")
    
    st.image("/Users/stephenthomas/Desktop/git_dashboard/Crypto-Prophecy/images/gt_all_crypto.png", caption="Worldwide interest in CryptoCurrency 2012 - 2021" )
    
    st.image("/Users/stephenthomas/Desktop/git_dashboard/Crypto-Prophecy/images/gt_nigeria_btc.png", caption="Nigerira Interest in Bitcoin 2012 - 2021")
    
    st.image("/Users/stephenthomas/Desktop/git_dashboard/Crypto-Prophecy/images/gt_el_sal.png", caption="El Salvador Interest in Bitcoin 2012 - 2021")

# This is the code for the Twitter API call and the query to do a full search of archives. The API is working but I can't figure out how to parse the info we want.   
if option == 'Tweet Counts':
    st.header("Tweet Counts")
    
    load_dotenv()
    
    tweepy_consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    tweepy_consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    tweepy_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    tweepy_access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

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


