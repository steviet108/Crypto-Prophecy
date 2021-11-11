import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
import json


st.title( "Crypto Prophet")


option = st.sidebar.selectbox("What is your Risk Appetite?", ( 'Low', 'Medium', 'High'), 1)

st.header(option)

r = requests.get(f"https://api.alternative.me/v2/ticker/?limit=100")
data = r.json()
st.write(data)
symbol = st.sidebar.text_input("coin", value='BTC', max_chars=5)
num_days = st.sidebar.slider('Amount to Invest', 1, 100000, 10)
sorted(d.items(), key=lambda x: x[1], reverse=True)

if option == 'Low':
    st.header("Investors Risk Appetite is Low")
    
if option == 'Medium':
    st.header("Investors Risk Appetite is Medium")
    
   
if option == 'High':
    st.header("Investors Risk Appetite is High")
    data_obj = json.loads(data)
    for i in range(50, 101):
        coin_index = str(i)
        st.write(data_obj[coin_index]['name'])
        st.write(data_obj[coin_index]['symbol'])
        
sorted(d.items(), key=lambda x: x[1], reverse=True)
    

    
       
        
    
    #st.write(data)
    