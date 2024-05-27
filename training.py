from functions import calculate_hourly_returns, add_all
from hmmlearn import hmm
import pickle, os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.impute import SimpleImputer
# impute the data instead of droping all rows with NaN values
import pandas as pd
import numpy as np
from scraping import get_stock_data, get_exchange_time



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
    path = os.path.join('models\pickles', name)
    with open(path , 'wb') as file:
        pickle.dump(model, file)
    with open(os.path.join('models', 'hmm_model.txt'), 'a') as file:
        file.write(f'{stock} - model updated in - {get_exchange_time()}\n')
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
    today = get_exchange_time()
    difference = today - last_update
    days = difference.days
    df = get_stock_data(stock, DAYS=days, interval='1h')
    returns = calculate_hourly_returns(df['Close'])
    path = f'models\pickles\{stock}hmm_model.pkl'
    with open(path , 'rb') as file:
        model = pickle.load(file)
    
    model.fit(returns)
    with open(path ,'wb' ) as file:
        pickle.dump(model)

    with open(os.path.join('models', 'hmm_model.txt'), 'a') as file:
        file.write(f'{stock} - model updated in - {today}\n')
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
    # impute the data instead of droping all rows with NaN values
    # df = df[['Open', 'High', 'Low', 'Close', 'sma-50', 'EMA', 'ADX', 'KLASS_VOL', 'RSI', 'Future_Close']]
    # imputer = SimpleImputer(strategy='mean')
    # df = imputer.fit_transform(df)
    df = df.dropna()
    x = df[['Open', 'High', 'Low', 'Close', 'Volume', 'sma-50', 'EMA', 'ADX', 'KLASS_VOL', 'RSI']]
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
    model = None # a deffolt value
    model_path = 'models\pickles\master_model.pkl'
    if os.path.exists(model_path) and os.path.getsize(model_path) > 0:
        try:
            # Load existing model
            with open(model_path, 'rb') as file:
                model = pickle.load(file)
            # print('master Model loaded successfully.')
        except EOFError:
            print('Error loading model. File might be corrupted. Creating a new model.')
    else:
        print('Model not found or is empty! Creating a new model.')

    # If model loading failed or didn't exist, create a new one
    if model is None:
        model = RandomForestRegressor(random_state=42)

    # Train (or refit) the model
    model.fit(X_train, y_train)
    # print('Model training complete.')

    # Save the updated model
    with open(model_path, 'wb') as file:
        pickle.dump(model, file)
    # print('master Model saved successfully.')

    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    # print(f'Mean Squared Error: {mse}')
    rmse = np.sqrt(mse)
    # print(f'Root Mean Squared Error: {rmse}')
    r2 = r2_score(y_test, y_pred)
    # print(f'R-squared: {r2}')
    
    with open(r'models\\model.txt', 'a') as file:
        file.write(f'{get_exchange_time()}  -  trained with {stock} data, score - {r2}\n')
    print('Saved master model')
# train_hmm_to_date('ASTS', datetime(2024, 5, 1))