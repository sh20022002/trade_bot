from functions import calculate_hourly_returns, add_all
from hmmlearn import hmm
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np
from scraping import get_stock_data
from datetime import date, datetime


def train_hmm(stock ,df):
    """
    Trains a Hidden Markov Model (HMM) using Gaussian emission distribution on the given stock data.

    Args:
        stock (str): The name of the stock.
        df (pandas.DataFrame): The dataframe containing the stock data.

    Returns:
        str: The name of the saved HMM model file.
    """
    returns = calculate_hourly_returns(df['Close'])
    n_states = 3
    model = hmm.GaussianHMM(n_components=n_states, covariance_type="diag", n_iter=1000)
    model.fit(returns)
    name = stock + 'hmm_model.pkl'
    path = r'models\\pickles' + name
    with open(path , 'wb') as file:
        pickle.dump(model, file)
    print('model saved.')
    return name


def train_hmm_to_date(stock, last_update):
    """
    Trains a Hidden Markov Model (HMM) using Gaussian emission distribution on the given stock data up to a specific date.

    Args:
        stock (str): The name of the stock.
        last_update (datetime): The date up to which the model should be trained.

    Returns:
        None
    """
    today = datetime.now()
    difference = today - last_update
    days = difference.days
    df = get_stock_data(stock, DAYS=days, interval='1h')
    returns = calculate_hourly_returns(df['Close'])
    path = f'models\pickles\{stock}hmm_model.pkl'
    with open(path , 'rb') as file:
        model = pickle.load(file)
    # cant load the model
    model.fit(returns)
    with open(path ,'wb' ) as file:
        pickle.dump(model)
    with open(r'models\\hmm_model.txt', 'a') as file:
        file.write(f'{stock} - model updated in - {today}')
    print('model saved.')


def pipline(stock):
    """
    Creates a data pipeline for training a regression model on stock data.

    Args:
        stock (str): The name of the stock.

    Returns:
        tuple: A tuple containing the training and testing data.
    """
    df = get_stock_data(stock, interval='1h', DAYS=365)
    df = add_all(df)
    df['Future_Close'] = df['Close'].shift(-1)
    x = df[['Open', 'High', 'Low', 'Close', 'sma-50', 'EMA', 'ADX', 'KLASS_VOL', 'RSI']]
    y = df['Future_Close']
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.15, random_state=42)
    return X_train, X_test, y_train, y_test


def train_p(X_train, X_test, y_train, y_test, stock):
    """
    Trains a regression model using the given training data and evaluates its performance on the testing data.

    Args:
        X_train (pandas.DataFrame): The features of the training data.
        X_test (pandas.DataFrame): The features of the testing data.
        y_train (pandas.Series): The target variable of the training data.
        y_test (pandas.Series): The target variable of the testing data.
        stock (str): The name of the stock.

    Returns:
        None
    """
    try:
        with open(r'models\\pickles\\master_model.pkl', 'wb') as file:
            model = pickle.load(file)
    except FileNotFoundError:
        print('file not found! creating a new model.')
        model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train) #
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'Mean Squared Error: {mse}')
    rmse = np.sqrt(mse)
    print(f'Root Mean Squared Error: {rmse}')
    r2 = r2_score(y_test, y_pred)
    print(f'R-squared: {r2}')
    file = 'master_model.pkl'
    with open(path , 'wb') as file:
        pickle.dump(model, file)
    with open(r'models\\model.txt', 'a') as file:
        file.write(f'{date.today()}  -  trained with {stock} data, score - {r2}')
    print('Saved model')
# train_hmm_to_date('ASTS', datetime(2024, 5, 1))