from functions import calculate_hourly_returns
from hmmlearn import hmm
import pickle



def train_hmm(stock ,df):
    returns = calculate_hourly_returns(df['Close'])
    n_statess=3
    model = hmm.GaussianHMM(n_components=n_statess, covariance_type="diag", n_iter=1000)
    model.fit(returns)
    name = stock + 'hmm_model.pkl'
    path = 'pickles/' + name
    with open(path , 'wb') as file:
        pickle.dump(model, file)
    print('saved model')
    return name

