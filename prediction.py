'''uses the model to predict stock vulability'''
import plots
import scraping
from functions import add_all, calculate_rsi
import pandas as pd
import training
import numpy as np
from hmmlearn import hmm
import pickle

def stock_and_tecnical(stock, interval='1h'):
    df = scraping.get_stock_data(stock, interval=interval, DAYS=365)
    df = add_all(df)
    
    return df

def rsi(stock):
    df = scraping.get_stock_data(stock)
    si = calculate_rsi(df)
    print(si)

def predict_next_state_and_probabilities(path_to_model, current_return):
    current_return = np.array(current_return).reshape(-1, 1)
    path = 'pickles/' + path_to_model
    with open(path, 'rb') as file:
        model = pickle.load(file)
    print(current_return)
    state_probs = model.predict_proba(current_return)
    # print(state_probs)
    next_state = np.argmax(state_probs)
    next_state_probs = state_probs[0]
    states = ['negative', 'neutral', 'positive']
    print(f"Predicted state for the next hour: {states[next_state]}")
    print(f"Probability of negative return: {next_state_probs[0]:.2f}")
    print(f"Probability of neutral return: {next_state_probs[1]:.2f}")
    print(f"Probability of positive return: {next_state_probs[2]:.2f}")


def main():
    stock = 'NVDA'
    # rsi(stock)
    df = predict_trend(stock)
    
    hidden_states, state_probabilitie = training.train_hmm(df)
    print(hidden_states, state_probabilitie)
    # plots.plot_stock(df, stock, show='all', interval='1h')
    

if __name__ == '__main__':
    main()