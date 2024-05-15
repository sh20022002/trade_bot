'''uses the model to predict stock vulability'''
# import plots.plot_stock as plot
from scraping import get_stock_data as stock_data
from functions import add_all
import pandas as pd

def predict_trend(stock):
    df = add_all(stock_data(stock))
    return df

def main():
    print(predict_trend('AAPL'))

if __name__ == '__main__':
    main()