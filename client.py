import server, database
import scraping
import streamlit as st
import time
import keyboard
import os
import psutil
import yfinance as yf
import pandas as pd



def initialize():
    # initialize the database
    sp500_compenies = scraping.get_tickers()

    # Index(['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry',

        #    'Headquarters Location', 'Date added', 'CIK', 'Founded']

    compenies = []

    sp500 = []

    for i in range(2):

        # print(sp500_compenies.index)

        compenies.append(sp500_compenies[1][i])

        compeny = server.compeny(sp500_compenies[2][i], sp500_compenies[1][i])

        compeny.GICS_Sector = sp500_compenies[3][i]

        compeny.GICS_Sub_Industry = sp500_compenies[4][i]

        compeny.Location = sp500_compenies[5][i]

        compeny.CIK = sp500_compenies[6][i]

        compeny.Founded = sp500_compenies[7][i]


        sp500.append(compeny)

    return sp500, compenies


stocks, compenies= initialize()


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


for compeny in stocks:

    if compeny.symbol == stock_ticker:

        st.write(f"Name: {compeny.compeny_name}")

        st.plotly_chart(compeny.show(interval, inicaitors))

        st.write(f"Location: {compeny.Location}")

        st.write(f"Founded: {compeny.Founded}")

        st.write(f"CIK: {compeny.CIK}")

        st.write(f"GICS Sector: {compeny.GICS_Sector}")

        st.write(f"GICS Sub-Industry: {compeny.GICS_Sub_Industry}")

        st.write(f"Price: {compeny.price}")

        st.write(f"Score: {compeny.score}")

        st.write(f"Sentiment: {compeny.sentiment}")

        st.write(f"Summary: {compeny.summary}")
        
        


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
 