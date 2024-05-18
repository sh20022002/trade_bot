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
    df = add_sma(df)
    df = add_ema(df)
    df = calculate_tr(df)
    df = calculate_adx(df)
    df = klass_vol(df)
    

    return df


def add_sma(df):

    # adds moving avg to df

    # smat= stock moving avraege time
    df['avg_high_low'] = (df['High'] + df['Low']) / 2
    smats = [50] # 100 and 200 alsw commen 
 
    for smat in smats:

        df[f'sma-{smat}'] = df['avg_high_low'].rolling(smat).mean()
    return df



def add_ema(df):

    window_size = 14  # Specify the window size for EMA calculation

    alpha = 2 / (window_size + 1)  # Calculate the smoothing factor (alpha)

    df['EMA'] = df['avg_high_low'].ewm(alpha=alpha, adjust=False).mean()
    return df



def calculate_rsi(df):

    window_size = 20
    delta = df.diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=window_size).mean()

    loss = (-delta.where(delta < 0, 0)).rolling(window=window_size).mean()


    rs = gain / loss

    rsi = 100 - (100 / (1 + rs))

    return rsi

    

def calculate_tr(df):

    tr1 = abs(df['High'] - df['Low'])

    tr2 = abs(df['High'] - df['Close'].shift())

    tr3 = abs(df['Low'] - df['Close'].shift())

    df['TR'] = np.maximum(np.maximum(tr1, tr2), tr3)
    return df


def calculate_adx(df):
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
    # (ln(high)- ln(low))**2
    #           2             -2(ln(2)-1)(ln(adj close) - ln(open)**2
    # print(df.columns)
    df['klass_vol'] = ((np.log(df['High']) - np.log(df['Low']))**2)/2 -(2*np.log(2) -1)*(np.log(df['Close'])-np.log(df['Open']))**2

    return df