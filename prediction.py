'''uses the model to predict stock vulnerability'''

import scraping
from functions import add_all, calculate_rsi
import training
import numpy as np
from hmmlearn import hmm
import pickle
import os

def stock_and_tecnical(stock, interval='1h'):
    '''
    Retrieves stock data and adds technical indicators to the dataframe.

    Parameters:
    - stock (str): The stock symbol.
    - interval (str): The time interval for the stock data. Default is '1h'.

    Returns:
    - df (pandas.DataFrame): The dataframe containing stock data with added technical indicators.
    '''
    df = scraping.get_stock_data(stock, interval=interval, DAYS=365)
    df = add_all(df)
    
    return df

def rsi(stock):
    '''
    Calculates the Relative Strength Index (RSI) for a given stock.

    Parameters:
    - stock (str): The stock symbol.

    Returns:
    - None
    '''
    df = scraping.get_stock_data(stock)
    si = calculate_rsi(df)
    print(si)

def predict_next_state_and_probabilities(path_to_model, current_return):
    '''
    Predicts the next state and probabilities of a stock return using a trained model.

    Parameters:
    - path_to_model (str): The path to the trained model file.
    - current_return (list): The current return value as a list.

    Returns:
    - None
    '''
    current_return = np.array(current_return).reshape(-1, 1)
    path = r'models\\pickles' + path_to_model
    # print(os.getcwd())
    with open(path, 'rb') as file:
        model = pickle.load(file)
    print(current_return)
    state_probs = model.predict_proba(current_return)
    next_state = np.argmax(state_probs)
    next_state_probs = state_probs[0]
    states = ['negative', 'neutral', 'positive']
    # print(f"Predicted state for the next hour: {states[next_state]}")
    state = states[next_state]
    probability = next_state_probs[next_state]
    # print(f"Probability of negative return: {next_state_probs[0]:.2f}")
    # print(f"Probability of neutral return: {next_state_probs[1]:.2f}")
    # print(f"Probability of positive return: {next_state_probs[2]:.2f}")
    return(state, probability)

