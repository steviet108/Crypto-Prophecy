import streamlit as st
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from nomics import Nomics
import json
import tweepy
import yfinance as yf
import matplotlib.pyplot as plt

# Load .env environment variables
load_dotenv()

# Header for main and sidebar
# st.title( "Crypto Prophet")
st.sidebar.title("CRYPTO PROPHET")

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
option = st.sidebar.selectbox("Select a Dashboard", ('Top 100 Cryptocurrencies by Market Cap', 'Coin Analysis', 'Deep Analysis', 'Cycle Analysis', 'Google Trends'), 0)
#option_1 = st.sidebar.text_input("coin", value="{symbol}", max_chars=5)
# This is the Header for each page
st.header(option)

# Pulls list of cryptocurrencies from Nomics
coin_df = "#" + top_cryptos_df['currency']
coin = top_cryptos_df['currency'] + "-USD"

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

    # Creates a dropdown list of cryptocurrencies based on top 100 list
    dropdown = st.multiselect("Select coin(s) to analyze", coin)
    dropdown_df = st.multiselect("Select coin(s) to analyze", coin_df)

    # Create start date for analysis
    start = st.date_input('Start', value = pd.to_datetime('today'))

    # Create end date for analysis
    end = st.date_input('End', value = pd.to_datetime('today'))

    # Line charts are created based on dropdown selection
    if len(dropdown) > 0: 
        coin_list = yf.download(dropdown,start,end)['Adj Close']

        # Display coin chart
        st.write('Selected Cryptocurrency Over Time')
        st.line_chart(coin_list)

        # Calculate daily returns
        daily_returns = coin_list.pct_change().dropna()
        # Convert to percentage
        daily_returns_pct = daily_returns * 100
        # Display the daily returns as a line chart
        st.write('Daily Returns')
        st.line_chart(daily_returns_pct)
        # Calculate cumulative returns
        cumulative_returns = (1 + daily_returns).cumprod()
        # Convert to a percentage
        cumulative_returns_pct = cumulative_returns * 100
        # Display the cumulative returs as a line chart
        st.write('Cumulative Returns')
        st.line_chart(cumulative_returns_pct)
        
        st.set_option('deprecation.showPyplotGlobalUse', False)
        

# This is the Deep Analysis option on dashboard dropdown.

if option == 'Deep Analysis':
    #st.sidebar.text_input("coin", value='BTC', max_chars=5)
    # Pull US dollar
    usd = yf.Ticker("DX-Y.NYB")

    # Creates a dropdown list of cryptocurrencies based on top 100 list
    dropdown = st.multiselect("Select 1 coin to analyze against USD", coin)

    # Create start date for analysis
    start = st.date_input('Start', value = pd.to_datetime('today'))

    # Create end date for analysis
    end = st.date_input('End', value = pd.to_datetime('today'))
    
    # Line charts are created based on dropdown selection
    if len(dropdown) > 0: 
        coin_list = yf.download(dropdown,start,end)['Adj Close']

        usd_df = usd.history(period="max").loc['2014-09-17':]
        usd_df = usd_df.drop(columns = ['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'])
        usd_hist = usd_df.rename(columns={'Close': 'USD'})
        comparison_df = yf.download(dropdown,start,end)['Adj Close']
        comparison_df = pd.DataFrame(comparison_df)
        comparison_df = comparison_df.rename(columns={'Adj Close': 'Coin'})
        
        # Ideally we want to change the column name from 'Adj Close' to user selected coin name.
        comparison_df = pd.concat([comparison_df, usd_hist], axis=1)

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
        
        # Some Markdown explaining what the probability distribution plot does.
        """
        This shows how volatile the coin is compared to the USD.
        The further the daily return values are spread around the mean,
        the more volatile the coin is. 
        
        """
        # Calculate the Variance using pandas 'var' function
        
        variance = daily_returns.var()
        st.subheader('Variance:')
        st.write(variance)

        # Markdown explaining what the variance does.
        """
        The variance measures the risk of a single asset by considering how far the 
        closing prices deviate from the mean. The greater the variance, the more volatile the asset.
        """
        st.subheader('Covariance:')
        
        covariance = (daily_returns['Coin']).cov(daily_returns['USD'])
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
        Measures the beta to determine how much the coin's return value is likely to change relative to changes
        in the overall market's return value. In this case we are using the USD as the market.
        A beta of 1.0 indicates the coin's return value will likely be exactly the same as that of the USD. 
        A beta greater than 1.0 indicates the coin's return value will likely be greater than the change in the
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

# This is the Cycle Analysis option on dashboard dropdown.
if option == 'Cycle Analysis':
    #st.header("Cycle Analysis")
    # path to static image cycle_analysis in the working folder.
    st.image('./images/cycle_analysis.png')
    
    # Markdown: analysis of bitcoin cycle
    """
    ### Summary of Bitcoin Market Cycle Analysis
    This Analysis of the Bitcoin Cycles helps answer two questions.
    
    1 - When will Bitcoin top out this current cycle?
    
    2 - What will the price be at the top of the current cycle?
    
    Analysis of the market cycles using statistics and data sheds light on several trends to answer these two questions and give investors an edge in this market.
    Cycles are measured from the start to the weekly low after the previous macro high. We have the Bitcoin chart from July 2010 to the present day on a logarithmic growth curve.
    A logarithmic growth curve is described as something that first exhibits explosive growth followed by an increasing taper until it reaches a plateau. Interestingly, 
    this trend is identified in nature, and Bitcoins growth has followed it very closely since it began trading around June of 2010. 
    This analysis uses past data to estimate the next macro high. 
    
    Cycle #1 Topped in June of 2011, with a closing price of around $18, and then went on to crash down to around $2.15, marking the end of cycle #1 and the
    begining of cycle #2. Cycle #1 was approximately 322 days, and there was a 37,750% increase in price. 
    
    Cycle #2 Rallied from 2.15$ to 1015$ in Dec. 2013, which was a 45,500% percent increase, and then went on to crash down to around $210 in January of 2015,
    marking the end of cycle #2. Cycle #2 was 750 days long and approximately 2.3 times longer than cycle #1 or 130% Longer. 
    
    Cycle #3 Started in December of 2018, one year after the previous cycle high, and rallied to around $20,000 per Bitcoin. This was a 9,000% percent increase. From the 
    beginning of cycle #3 to the cycle high and was 1070 days, which is 1.4 times longer or 43% longer than the previous cycle. 
    
    To date, we have three cycles to analyze, which allows one to postulate several trends. The cycles are getting longer, but the rate that they are getting longer
    is decreasing. Cycle #1 was 322 days from bottom to top, cycle #2 was 750 days or 130% longer than the previous cycle, and cycle #3 was 
    1070 days or 43% longer than previous cycle. These trends give insight into when the current cycle could top and what the price might be.
    
    We know that the cycles are getting longer at a decreasing rate and if cycle #3 was 1070 days and 43% longer than the previous cycle, we can postulate 
    cycle #4 could be longer than #3 at a reduced rate of lengthing. If we cut cycle #3's rate of lengthing in half and applied 20% to cycle #4's, then cycle #4 could be 
    200 days longer than cycle #3. It is interesting to not that currently, as of mid November 2021, cycle #4 is as long as cycle #3, around 1070 days. Adding 200 days to today would
    put the current cycle top right around mid-May 2022. If we did the same thing but applied 10% of cycle #3's rate of lengthing, the cycle could top around March 2022. This analysis  
    indicates that cycle #4 could top somewhere in between March and May 2022.

    With a rough idea of when Bitcoin will top, we can look at potential price targets based on those dates. Based on Bitcoin's Logarithmic curve chart
    Bitcoin historically tops when its touches the upper end of the red zone or band. This was seen in the last 3 cycles. Cycle #1 closed a weekly candle around 18$, cycle #2 closed around $1,000 and
    cycle #3 closed around $20,000. Extrapolating the historical data to the dates of when the current cycle could top, gives some potential targets.The first is a weekly candle 
    closing around $150,000 at the beginning of March, and the second is a weekly candle closing in the middle of May around $175,000. 
    
    As Mark Twain put it "History doesn't repeat but it does rhyme".
    """



# This is the Google Trends option on dashboard dropdown, and we can make it dynamic for each coin the api call gives us.    
if option == 'Google Trends':
    # Markdown: Explanation of how to read the folowing Google Trends charts.
    """Numbers on the Y-axis represent search interest relative to the highest point on the chart for the given region and time.
    A value of 100 is the peak popularity for the term. A value of 50 means that the term is half as popular. 
    A score of 0 means there was not enough data for this term."""
    # Google Trends chart.
    st.image('./images/Google_Trends.png', caption="Worldwide Interest in Bitcoin 2012 - 2021")
    
    #st.image('./images/global_interest_btc.png', caption="Worldwide Interest in Bitcoin by Region 2012 - 2021")

    st.image('./images/gt_all_crypto.png', caption="Worldwide interest in CryptoCurrency 2012 - 2021" )
    
    st.image('./images/gt_nigeria_btc.png', caption="Nigerira Interest in Bitcoin 2012 - 2021")
    
    st.image('./images/gt_el_sal.png', caption="El Salvador Interest in Bitcoin 2012 - 2021")