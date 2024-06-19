''' 
This module contains various functions for analyzing stock data and calculating technical indicators.

Functions:
- summery(strategy): Returns a formatted string with strategy information.
- add_all(df): Adds various technical indicators to the given DataFrame.
- add_sma(df): Adds the Simple Moving Average (SMA) to the given DataFrame.
- add_ema(df): Adds the Exponential Moving Average (EMA) to the given DataFrame.
- calculate_rsi(df, window=14): Calculate the Relative Strength Index (RSI) for a given DataFrame.
- calculate_tr(df): Calculates the True Range (TR) for the given DataFrame.
- calculate_adx(df): Calculates the Average Directional Index (ADX) for the given DataFrame.
- klass_vol(df): Calculates the Klass Volatility (klass_vol) for the given DataFrame.
- calculate_hourly_returns(stock_prices): Calculates the hourly returns for the given stock prices.
- chack_last_update_of_model(stock): Checks the last update of the model for a specific stock.

Note: This module requires the 'pandas', 'numpy', and 'scraping' modules to be imported.
'''

import pandas as pd 
import numpy as np
from scraping import get_stock_data, get_exchange_time



def summery(strategy):
    '''
    Returns a formatted string with strategy information.

    Parameters:
    strategy (str): The strategy in the format "term-res-limit-rid-prediction".

    Returns:
    str: The formatted string with strategy information.

    Example:
    >>> summery("short-sma50-200-100-negative")
    'short'
    '''
    try:
        term, res, limit, rid, prediction = strategy.split('-')
    except:
        return 'format: short-sma50-200-100-negative'
    return term

def add_all(df):
    '''
    Adds various technical indicators to the given DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing stock data.

    Returns:
    pd.DataFrame: The DataFrame with added technical indicators.

    Example:
    >>> df = pd.DataFrame({'Open': [100, 110, 105], 'High': [120, 115, 125], 'Low': [90, 100, 95], 'Close': [110, 105, 120]})
    >>> add_all(df)
       Open  High  Low  Close  avg_high_low  sma-50  EMA   TR  ADX  klass_vol  RSI
    0   100   120   90    110         105.0     NaN  NaN  NaN  NaN        NaN  NaN
    1   110   115  100    105         107.5     NaN  NaN  NaN  NaN        NaN  NaN
    2   105   125   95    120         110.0     NaN  NaN  NaN  NaN        NaN  NaN
    '''
    df = add_sma(df)
    df['EMA'] = add_ema(df)
    df['TR'] = calculate_tr(df)
    df['ADX'] = calculate_adx(df)
    df['KLASS_VOL'] = klass_vol(df)
    df['RSI'] = calculate_rsi(df)
    try:
        df = df.drop(['Dividends','Stock Splits', 'avg_high_low', 'TR'], axis=1)
    except KeyError:
        df = df.drop(['avg_high_low', 'TR'], axis=1)
    return df

def add_sma(df):
    '''
    Adds the Simple Moving Average (SMA) to the given DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing stock data.

    Returns:
    pd.DataFrame: The DataFrame with added SMA columns.

    Example:
    >>> df = pd.DataFrame({'Open': [100, 110, 105], 'High': [120, 115, 125], 'Low': [90, 100, 95], 'Close': [110, 105, 120]})
    >>> add_sma(df)
       Open  High  Low  Close  avg_high_low  sma-50
    0   100   120   90    110         105.0     NaN
    1   110   115  100    105         107.5     NaN
    2   105   125   95    120         110.0     NaN
    '''
    df['avg_high_low'] = (df['High'] + df['Low']) / 2
    smats = [20, 50, 100] # 100 and 200 also common
    for smat in smats:
        df[f'SMA{smat}'] = df['avg_high_low'].rolling(smat).mean()
    return df

def add_ema(df):
    '''
    Adds the Exponential Moving Average (EMA) to the given DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing stock data.

    Returns:
    pd.DataFrame: The DataFrame with added EMA column.

    Example:
    >>> df = pd.DataFrame({'Open': [100, 110, 105], 'High': [120, 115, 125], 'Low': [90, 100, 95], 'Close': [110, 105, 120]})
    >>> add_ema(df)
       Open  High  Low  Close  avg_high_low  sma-50         EMA
    0   100   120   90    110         105.0     NaN  105.000000
    1   110   115  100    105         107.5     NaN  106.666667
    2   105   125   95    120         110.0     NaN  108.333333
    '''
    window_size = 50
    alpha = 2 / (window_size + 1)
    ema = df['avg_high_low'].ewm(alpha=alpha, adjust=False).mean()
    return ema




def calculate_rsi(df, window=14):
    """
    Calculate the Relative Strength Index (RSI) for a given DataFrame.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing the 'Close' prices.
    - window (int): The number of periods to use for calculating the RSI. Default is 14.

    Returns:
    - rsi (pandas.Series): The calculated RSI values.

    """
    # Calculate price changes
    delta = df['Close'].diff()
    
    # Calculate gains and losses
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    
    # Calculate the average gain and loss
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    
    # Calculate the Relative Strength (RS)
    rs = avg_gain / avg_loss
    
    # Calculate the RSI
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_tr(df):
    '''
    Calculates the True Range (TR) for the given DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing stock data.

    Returns:
    pd.DataFrame: The DataFrame with added TR column.

    Example:
    >>> df = pd.DataFrame({'High': [120, 115, 125], 'Low': [90, 100, 95], 'Close': [110, 105, 120]})
    >>> calculate_tr(df)
       High  Low  Close   TR
    0   120   90    110  NaN
    1   115  100    105  25.0
    2   125   95    120  30.0
    '''
    tr1 = abs(df['High'] - df['Low'])
    tr2 = abs(df['High'] - df['Close'].shift())
    tr3 = abs(df['Low'] - df['Close'].shift())
    tr = np.maximum(np.maximum(tr1, tr2), tr3)
    return tr

def calculate_adx(df):
    '''
    Calculates the Average Directional Index (ADX) for the given DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing stock data.

    Returns:
    pd.DataFrame: The DataFrame with added ADX column.

    Example:
    >>> df = pd.DataFrame({'High': [120, 115, 125], 'Low': [90, 100, 95], 'Close': [110, 105, 120]})
    >>> calculate_adx(df)
       High  Low  Close   TR  ADX
    0   120   90    110  NaN  NaN
    1   115  100    105  25.0  NaN
    2   125   95    120  30.0  NaN
    '''
    df_temp = df.copy()
    window_size = 14
    df_temp['DMplus'] = np.where((df['High'] - df['High'].shift()) > (df['Low'].shift() - df['Low']), 
                              np.maximum(df['High'] - df['High'].shift(), 0), 0)
    df_temp['DMminus'] = np.where((df['Low'].shift() - df['Low']) > (df['High'] - df['High'].shift()), 
                               np.maximum(df['Low'].shift() - df['Low'], 0), 0)
    df_temp['ATR'] = df['TR'].rolling(window=window_size).mean()
    df_temp['DMplus_smoothed'] = df_temp['DMplus'].rolling(window=window_size).mean()
    df_temp['DMminus_smoothed'] = df_temp['DMminus'].rolling(window=window_size).mean()
    df_temp['DIplus'] = 100 * (df_temp['DMplus_smoothed'] / df_temp['ATR'])
    df_temp['DIminus'] = 100 * (df_temp['DMminus_smoothed'] / df_temp['ATR'])
    df_temp['DX'] = 100 * (np.abs(df_temp['DIplus'] - df_temp['DIminus']) / (df_temp['DIplus'] + df_temp['DIminus']))
    ADX = df_temp['DX'].rolling(window=window_size).mean()
    return ADX

def klass_vol(df):
    '''
    Calculates the Klass Volatility (klass_vol) for the given DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame containing stock data.

    Returns:
    pd.DataFrame: The DataFrame with added klass_vol column.

    Example:
    >>> df = pd.DataFrame({'High': [120, 115, 125], 'Low': [90, 100, 95], 'Close': [110, 105, 120], 'Open': [100, 110, 105]})
    >>> klass_vol(df)
       High  Low  Close  Open  klass_vol
    0   120   90    110   100        NaN
    1   115  100    105   110        NaN
    2   125   95    120   105        NaN
    '''
    klass_vol = ((np.log(df['High']) - np.log(df['Low']))**2)/2 -(2*np.log(2) -1)*(np.log(df['Close'])-np.log(df['Open']))**2
    return klass_vol

def calculate_hourly_returns(stock_prices):
    '''
    Calculates the hourly returns for the given stock prices.

    Parameters:
    stock_prices (pd.Series): The hourly stock prices.

    Returns:
    np.ndarray: The hourly returns.

    Example:
    >>> stock_prices = pd.Series([100, 110, 105, 120, 115])
    >>> calculate_hourly_returns(stock_prices)
    array([[ 0.1],
           [-0.04545455],
           [ 0.14285714],
           [-0.04166667]])
    '''
    returns = stock_prices.pct_change().dropna()
    return returns.values.reshape(-1, 1)


def chack_last_update_of_model(stock):
    """
    Retrieves the last update datetime of the model trained with the specified stock data.

    Args:
        stock (str): The stock symbol or identifier.

    Returns:
        datetime.datetime or None: The datetime of the last update if found, None otherwise.
    """
    with open(r'models\\model.txt', 'r') as file:
        lines = file.readlines()
        for line in reversed(lines):
            if f'trained with {stock} data' in line:
                datetime_str = line.split(' - ')[0].strip()
                entry_datetime = get_exchange_time()
                return entry_datetime
    return None



def chack_last_update_of_hmm_model(stock, interval):
    """
    Retrieves the last update datetime of the hmm model trained with the specified stock data.

    Args:
        stock (str): The stock symbol or identifier.

    Returns:
        datetime.datetime or None: The datetime of the last update if found, None otherwise.
    """
    
    with open(r'models\\hmm_model.txt', 'r') as file:
        lines = file.readlines()
        for line in reversed(lines):
            if f'{stock} - {interval} - model updated in' in line:
                datetime_str = line.split(' - ')[2].strip()
                entry_datetime = get_exchange_time()
                return entry_datetime
    return None


def generate_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
