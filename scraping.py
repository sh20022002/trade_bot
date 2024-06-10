'''all web scraping functions'''
from datetime import timedelta 
import pandas as pd
import yfinance as yf
import pytz, datetime
import requests
from api_keys import exchange_api_key


def get_stock_sum(stock):
    '''Get the latest news related to stocks.'''
    pass

def current_stock_price(symbol):
    '''Get the current stock price for a given symbol.'''
    return 0

def get_stock_data(stock, DAYS=365, interval='1h'):
    '''
    Get historical stock data for a given stock symbol.

    Parameters:
    - stock (str): The stock symbol.
    - DAYS (int): The number of days of historical data to retrieve. Default is 100.
    - interval (str): Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
    
    Returns:
    - DataFrame: A pandas DataFrame containing the historical stock data.
    '''
    end_date = get_exchange_time()##
    
    start_date = end_date - timedelta(DAYS)  # days before the end date
    stock_ticker = yf.Ticker(stock)
    df = stock_ticker.history(start=start_date, end=end_date, interval=interval)
    if interval == '1h':
        df = df.reset_index('Datetime')
    else:
        df.reset_index(inplace=True)
        df.rename(columns={'Date': 'Datetime'}, inplace=True)
    return df

def get_tickers():
    tickers = pd.read_html(
    'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    return tickers[0].values

def get_exchange_time():
    # Define the timezone for New York
    ny_timezone = pytz.timezone('America/New_York')

    # Get the current time in New York
    ny_time = datetime.datetime.now(ny_timezone)

    # Format the time similar to yfinance format
    # formatted_ny_time = ny_time.strftime('%Y-%m-%d %H:%M:%S')

    return (ny_time)

def get_exchange_rate(from_currency, to_currency):
    
    url = f'https://v6.exchangerate-api.com/v6/{api_keys.exchange_api_key}/latest/{from_currency}'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        exchange_rate = data['conversion_rates'][to_currency]
        return exchange_rate
    else:
        return EOFError


rate = get_exchange_rate(from_currency, to_currency)
return rate