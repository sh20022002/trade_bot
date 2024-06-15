import server, database
import scraping
import streamlit as st
import time
import keyboard
import os
import psutil
import yfinance as yf
import pandas as pd





stocks, compenies= initialize()

def client_page(user):
    st.title("SmartTraid")
    st.title("The Future of Trading.")
    st.sidebar.title("Analyze Stock")
    stock_ticker = st.sidebar.selectbox("stock", compenies)
    inicaitors = st.sidebar.multiselect('Inicaitors', ['Volume','sma-50', 'EMA', 'ADX', 'RSI'])
    interval = st.sidebar.radio('Interval', ['Day', 'Hour'])
    if interval == 'Day':
        interval = '1d'
    else:
        interval = '1h'
    
    st.sidebar.title("account")
    st.sidebar.write(f"Name: {user.name}")
    st.sidebar.write(f"ID: {user.ID} ")
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
    exit_app = st.button("Shut Down")
    if exit_app:
        time.sleep(5)
        keyboard.press_and_release('ctrl+w')
        pid = os.getpid()
        p = psutil.Process(pid)
        p.terminate()
#st.sidebar.radio('Interval', ['Day', 'Hour'])

