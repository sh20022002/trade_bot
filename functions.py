''' all none class functions'''
import pandas as pd 
import numpy as np

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
       Open  High  Low  Close  avg_high_low  sma-50  EMA   TR  ADX  klass_vol
    0   100   120   90    110         105.0     NaN  NaN  NaN  NaN        NaN
    1   110   115  100    105         107.5     NaN  NaN  NaN  NaN        NaN
    2   105   125   95    120         110.0     NaN  NaN  NaN  NaN        NaN
    '''
    df = add_sma(df)
    df = add_ema(df)
    df = calculate_tr(df)
    df = calculate_adx(df)
    df = klass_vol(df)
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
    smats = [50] # 100 and 200 also common
    for smat in smats:
        df[f'sma-{smat}'] = df['avg_high_low'].rolling(smat).mean()
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
    df['EMA'] = df['avg_high_low'].ewm(alpha=alpha, adjust=False).mean()
    return df




def calculate_rsi(df, window=14):
    """
    Calculate Relative Strength Index (RSI)

    Parameters:
    df (pd.DataFrame): DataFrame which contain the asset prices.
    window (int): The window period. Default window is 14.

    Returns:
    pd.Series: A pandas Series containing the RSI values.
    """
    # Calculate the price change
    delta = df.diff()

    # Make two series: one of gains, the other of losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)

    # Calculate the average gain and average loss
    avg_gain = gains.rolling(window=window).mean()
    avg_loss = losses.rolling(window=window).mean()

    # Calculate RS
    rs = avg_gain / avg_loss

    # Calculate RSI
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
    df['TR'] = np.maximum(np.maximum(tr1, tr2), tr3)
    return df

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
    df['ADX'] = df_temp['DX'].rolling(window=window_size).mean()
    return df

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
    df['klass_vol'] = ((np.log(df['High']) - np.log(df['Low']))**2)/2 -(2*np.log(2) -1)*(np.log(df['Close'])-np.log(df['Open']))**2
    return df

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


