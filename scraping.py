'''all web scraping functions'''
from datetime import date, timedelta
# from pandas_datareader import data as pdr

import pandas as pd
import yfinance as yf


def get_stock_news():
    '''Get the latest news related to stocks.'''
    pass

def current_stock_price(symbol):
    '''Get the current stock price for a given symbol.'''
    pass
    

def get_stock_data(stock, DAYS=100, interval='1d'):
    '''
            Get historical stock data for a given stock symbol.

            Parameters:
            - stock (str): The stock symbol.
            - DAYS (int): The number of days of historical data to retrieve. Default is 100.
            -interval Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
            Returns:
            - DataFrame: A pandas DataFrame containing the historical stock data.
    '''
    end_date = date.today()
    start_date = end_date - timedelta(DAYS)  # days before the end date
    stock_ticker = yf.Ticker(stock)
    df = stock_ticker.history(start=start_date, end=end_date, interval=interval)
    if (interval == '1h'):
         df = df.reset_index('Datetime')
        
    else:
        
        df.reset_index(inplace=True)
        df.rename(columns={'Date': 'Datetime'}, inplace=True)
    
    return df

def main():
    res = get_stock_data('AAPL', interval='1h')
    print(res.head(10))


if __name__=='__main__':
    main()