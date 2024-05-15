'''all web scraping functions'''
from datetime import date, timedelta
# from pandas_datareader import data as pdr
from api_keys import key
from datetime import date, timedelta
import pandas as pd
import yfinance as yf


def get_stock_news():
    '''Get the latest news related to stocks.'''
    pass

def current_stock_price(symbol):
    '''Get the current stock price for a given symbol.'''
    pass
    

def get_stock_data(stock, DAYS=100):
    '''
            Get historical stock data for a given stock symbol.

            Parameters:
            - stock (str): The stock symbol.
            - DAYS (int): The number of days of historical data to retrieve. Default is 100.

            Returns:
            - DataFrame: A pandas DataFrame containing the historical stock data.
    '''
    end_date = date.today()
    start_date = end_date - timedelta(DAYS)  # days before the end date
    df = yf.download(stock, start_date, end_date, )
    df = df.sort_values(by=['Date'])  # sort the data from newest to oldest
    df = df.reset_index('Date')
    return df