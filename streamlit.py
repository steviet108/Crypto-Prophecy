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
import matplotlib.pyplot as plt

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
# num_days = st.sidebar.slider('Amount to Invest', 1, 100000, 10)

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

    # Pull US dollar
    usd = yf.Ticker("DX-Y.NYB")

    # Creates a dropdown list of cryptocurrencies based on top 100 list
    select_usd = st.checkbox("Select to begin (USD)", usd)

    # Pulls list of cryptocurrencies from Alpaca
    coin = top_cryptos_df['currency'] + "-USD"

    # Creates a dropdown list of cryptocurrencies based on top 100 list
    dropdown = st.multiselect("Select coin(s) to analyze against USD", coin)

    # Create start date for analysis
    start = st.date_input('Start', value = pd.to_datetime('today'))

    # Create end date for analysis
    end = st.date_input('End', value = pd.to_datetime('today'))

    # Line charts are created based on dropdown selection
    if len(dropdown) > 0: 
        coin_list = yf.download(dropdown,start,end)['Adj Close']
        # st.write('Selected list of cryptocurrencies')
        # st.write(coin_list)
        #usd_list = yf.download(usd,start, end)['Adj Close']
        # st.write('USD')
        # st.write(usd_list)

        # Display USD Chart
        #st.write('USD Over Time')
        #st.line_chart(usd_list)

        # Display coin chart
        st.write('Selected Cryptocurrency Over Time')
        st.line_chart(coin_list)

        # usd_coin = pd.concat([usd_list, coin_list], axis=1)
        # st.write('USD vs. Selected Cryptocurrency Over Time')
        # st.write(usd_coin)
        # st.line_chart(usd_coin)

        usd_df = usd.history(period="max").loc['2014-09-17':]
        usd_df = usd_df.drop(columns = ['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'])
        usd_hist = usd_df.rename(columns={'Close': 'USD'})
        comparison_df = yf.download(dropdown,start,end)['Adj Close']
        comparison_df = pd.DataFrame(comparison_df)
        comparison_df = comparison_df.rename(columns={'Adj Close': 'Coin'})
        # Ideally we want to change the column name from 'Adj Close' to user selected coin name.
        comparison_df = pd.concat([comparison_df, usd_hist], axis=1)
        st.line_chart(comparison_df['Coin'])


        # Calculate daily returns
        daily_returns = comparison_df.pct_change().dropna()
        # Convert to percentage
        daily_returns_pct = daily_returns * 100
        # Display the daily returns as a line chart
        st.write('Daily Returns Compared to USD (%)')
        st.line_chart(daily_returns_pct)
        # Calculate cumulative returns
        cumulative_returns = (1 + daily_returns).cumprod()
        # Convert to a percentage
        cumulative_returns_pct = cumulative_returns * 100
        # Display the cumulative returs as a line chart
        st.write('Cumulative Returns Compared to USD (%)')
        st.line_chart(cumulative_returns_pct)
        # Calculate the standard deviation
        standard_deviation = daily_returns.std()
        #st.box_chart(standard_deviation)
        # Calculate the annualized standard deviation
        annualized_standard_deviation = standard_deviation * np.sqrt(365)
        # Calculate average annual return (crypto trades everyday of the year)
        average_annual_return = daily_returns.mean() * 365
        # Calculate the Sharpe Ratio
        sharpe_ratio = average_annual_return / annualized_standard_deviation
        # Print Sharpe Ratio
        st.write('Sharpe Ratios')
        st.bar_chart(sharpe_ratio)
        
        # Display Probabilty Distribution
        st.write('Probability Distributions')
        #fig, ax = plt.subplots()
        #ax.hist(daily_returns)
        #st.pyplot(fig)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        daily_returns.hist()
        plt.show()
        st.pyplot()
        """
        This shows how volatile the coin is compared to the USD.
        The further the daily return values are spread around the mean,
        the more volatile the coin is. 
        """
        # Calculate the Variance using pandas 'var' function
        
        variance = daily_returns.var()
        st.subheader('Variance:')
        st.write(variance)

        
        
        """
        The variance measures the risk of a single asset by considering how far the 
        closing prices deviate from the mean. The greater the variance, the more volatile the asset.
        """
        st.subheader('Covariance:')
        
        covariance = daily_returns['Coin'].cov(daily_returns['USD'])
        st.write(f'{covariance: .10f}')
        """
        Calculate the covariance to determine if the value of the coin and the USD tend to move in the same direction.
        If the covariance is positive, they tend to move in a similar direction.
        """

        st.subheader('Beta:')
        # Calculate the beta of the coin to determine the volatility compared to USD.
        coin_beta = daily_returns['Coin'].cov(daily_returns['USD']) / daily_returns['USD'].var()
        st.write(f'The beta is {coin_beta}')
        """
        Measure the beta to determine how much the coin's return value is likely to change relative to changes
        in the overall market's return value. In this case we are using the USD as the market.
        A beta of 1.0 indicates the coin's return value will likely be exactly the same as that of the USD. 
        A beta greater than 1.0 indicates the coin's retuen value will likely be greater than the change in the
        value of the USD.
        A negative beta indicates that if the return value of the USD increases, 
        the return value of the coin decreases, and vice versa."""
        
        ### Density Plot TBD ###
        
        # Calculate and plot the rolling metrics of the coin

        # Calculate the rolling 30 day variance of the USD 
        usd_rolling_30_variance = comparison_df['USD'].rolling(window=30).var()
        coin_rolling_30_variance = comparison_df['Coin'].rolling(window=30).var()
        #USD 30 day rolling variance
        st.write('Rolling 30-Day Variance of USD Returns')
        st.line_chart(usd_rolling_30_variance)

        st.write('Rolling 30-Day Variance of Coin Returns')
        st.line_chart(coin_rolling_30_variance)

        # Calculate the rolling 30-day covariance between Coin and the USD

        ### ERROR WHEN INTEGRATING WITH STREAMLIT. 
        coin_rolling_30_covariance = comparison_df['Coin'].rolling(window=30).cov(comparison_df['USD'].rolling(window=30))


        # Create the plot for Coin's 30-day rolling covariance
        st.write('Rolling 30-Day Covariance of Coin Returns vs. USD Returns')
        st.line_chart(coin_rolling_30_covariance)
        
        # Calculate the rolling beta by dividing Coin’s 30-day rolling covariance
        # by the 30-day rolling variance of the USD
        coin_rolling_30_beta = coin_rolling_30_covariance / usd_rolling_30_variance

        # Create the plot for Coin's 30-day rolling beta
        st.write('Coin - Rolling 30-Day Beta')
        st.line_chart(coin_rolling_30_beta)
        

        # Overlay plot of daily prices and rolling average. Not sure about overlay plot in streamlit.
        #ax = comparison_df['Coin'].plot(figsize=(10,7), title='Coin Daily Prices vs 90-Day Rolling Average')
        #comparison_df['Coin'].rolling(window=90).mean().plot(ax=ax)
        #ax.legend(['Daily Prices', '90-Day Rolling Average'])
    






        # Calculate and plot the rolling metrics of the coin
        #ax = btc_df['Close'].plot(figsize=(10,7), title='Coin Daily Prices vs 90-Day Rolling Average')
        #btc_df['Close'].rolling(window=90).mean().plot(ax=ax)
        #ax.legend(['Daily Prices', '90-Day Rolling Average'])
        ### We can add more rolling average metrics if we have time. 
        # ie. different time periods and/or rolling standard deviation. 
        # Rolling variance, covariance, beta

        ### This is me trying to get the monte carlo simulation to work: ###
        #usd_btc_df_original = pd.concat([btc_df, usd_df], axis=1)
        #usd_btc_df_original = usd_btc_df_original.rename(columns={'Close':'close'}).dropna()
        # Monte Carlo
        #daily_returns_mc = daily_returns_df.rename(columns={'BTC':'daily_return','USD':'daily_return'})
        #MC_fiveyear = MCSimulation(
            #portfolio_data = btc_df,
            #weights = [.60,.40],
            #num_simulation = 500,
            #num_trading_days = 365*5
#)

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

