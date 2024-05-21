from functions import calculate_hourly_returns
from hmmlearn import hmm
import pickle

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
    path = r'pickles' + name
    with open(path , 'wb') as file:
        pickle.dump(model, file)
    print('Saved model')
    return name

