import Traiding_custamer, database
import scraping
import streamlit as st
import time
import keyboard
import os
import psutil
import yfinance as yf
import pandas as pd


sp500_compenies = scraping.get_tickers()
# Index(['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry',
    #    'Headquarters Location', 'Date added', 'CIK', 'Founded']

sp500 = []
for i in range(len(sp500_compenies[0])):
    
sp500_symbols = scraping.get_tickers()


# Set the title of the app
st.title("Trading Platform")
st.sidebar.title("Analyze Stock")
# st.sidebar.subheader("Enter the stock ticker")
stock_ticker = st.sidebar.selectbox("stock", sp500_compenies)
inicaitors = st.sidebar.multiselect('Inicaitors', ['Volume','sma-50', 'EMA', 'ADX', 'RSI'])
interval = st.sidebar.radio('Interval', ['Day', 'Hour'])
if interval == 'Day':
    interval = '1d'
else:
    interval = '1h'

# block
st.write(f"Stock: {stock_ticker}")
# st.plotly_chart(stock.show(interval, inicaitors))

# exit button
exit_app = st.button("Shut Down")
if exit_app:
    # Give a bit of delay for user experience
    time.sleep(5)
    # Close streamlit browser tab
    keyboard.press_and_release('ctrl+w')
    # Terminate streamlit python process
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()
 