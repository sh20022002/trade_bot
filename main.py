import Traiding_custamer, database
import scraping
import streamlit as st
import time
import keyboard
import os
import psutil
import yfinance as yf
import pandas as pd


compenies = []
def initialize():
    # initialize the database
    sp500_compenies = scraping.get_tickers()
    # Index(['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry',
        #    'Headquarters Location', 'Date added', 'CIK', 'Founded']

    sp500 = []
    for i in range(len(sp500_compenies[0])):
        compenies.append(sp500_compenies[2][i])
        compeny = Traiding_custamer.compeny(sp500_compenies[2][i], sp500_compenies[1][i])
        compeny.GICS_Sector = sp500_compenies[3][i]
        compeny.GICS_Sub_Industry = sp500_compenies[4][i]
        compeny.Location = sp500_compenies[5][i]
        compeny.CIK = sp500_compenies[6][i]
        compeny.Founded = sp500_compenies[7][i]

        # Save the compeny to the database
        database.save_compeny(compeny)
        hourly_returns = compeny.probability_of_returns('1h')
        daily_returns = compeny.probability_of_returns('1d')



# Set the title of the app
st.title("Trading Platform")

st.sidebar.title("Analyze Stock")
# st.sidebar.subheader("Enter the stock ticker")
stock_ticker = st.sidebar.selectbox("stock", compenies)
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
 