''' all none class functions'''
import pandas as pd 

import numpy as np

def summery(strategy):

    '''should have to get a formated string with strategy in a logic operatins
    

    short\long-none\sma\50\100\200-none\pricer-none\price-prediction'''

    try:

        term, res, limit, rid, prediction = strategy.split('-')

    except:

        return 'format: short-sma50-200-100-negative'

    return term + res

def add_all(df):
    df = add_moa(df)
    df = add_ema(df)
    return df


def add_moa(df):

    # adds moving avg to df

    # smat= stock moving avraege time
    df['avg_high_low'] = (df['High'] + df['Low']) / 2
    smats = [50, 100, 200]

    for smat in smats:

        df[f'moa-{smat}'] = df['avg_high_low'].rolling(smat).mean()
    return df



def add_ema(df):

    window_size = 14  # Specify the window size for EMA calculation

    alpha = 2 / (window_size + 1)  # Calculate the smoothing factor (alpha)

    df['EMA'] = df['avg_high_low'].ewm(alpha=alpha, adjust=False).mean()
    return df



def calculate_rsi(df):

    window_size = 14
    delta = df.diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=window_size).mean()

    loss = (-delta.where(delta < 0, 0)).rolling(window=window_size).mean()


    rs = gain / loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_dx(df):

    window_size = 14

    tr = df['TR']

    atr = tr.rolling(window=window_size).mean()

    dx = 100 * (atr / df['ADX'])

    return dx
    

def calculate_tr(df):

    tr1 = abs(df['High'] - df['Low'])

    tr2 = abs(df['High'] - df['Close'].shift())

    tr3 = abs(df['Low'] - df['Close'].shift())

    df['TR'] = np.maximum(np.maximum(tr1, tr2), tr3)
    return df


def calculate_adx(df):

    window_size = 14
    
    tr1 = abs(df['High'] - df['Low'])

    tr2 = abs(df['High'] - df['Close'].shift())

    tr3 = abs(df['Low'] - df['Close'].shift())
    df['TR'] = np.maximum(np.maximum(tr1, tr2), tr3)

    df['DMplus'] = np.where((df['High'] - df['High'].shift()) > (df['Low'].shift() - df['Low']), 

                              np.maximum(df['High'] - df['High'].shift(), 0), 0)
    df['DMminus'] = np.where((df['Low'].shift() - df['Low']) > (df['High'] - df['High'].shift()), 

                               np.maximum(df['Low'].shift() - df['Low'], 0), 0)

    df['ATR'] = df['TR'].rolling(window=window_size).mean()
    df['DMplus_smoothed'] = df['DMplus'].rolling(window=window_size).mean()
    df['DMminus_smoothed'] = df['DMminus'].rolling(window=window_size).mean()

    df['DIplus'] = 100 * (df['DMplus_smoothed'] / df['ATR'])
    df['DIminus'] = 100 * (df['DMminus_smoothed'] / df['ATR'])

    df['DX'] = 100 * (np.abs(df['DIplus'] - df['DIminus']) / (df['DIplus'] + df['DIminus']))
    df['ADX'] = df['DX'].rolling(window=window_size).mean()

    return df['ADX']

