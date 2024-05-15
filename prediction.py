'''uses the model to predict stock vulability'''
import plots
import scraping
from functions import add_all
import pandas as pd

def predict_trend(stock):
    df = scraping.get_stock_data(stock, 300)
    df = add_all(df)
    return df

def main():
    stock = 'AAPL'
    df = predict_trend(stock)
    plots.plot_stock(df, stock)
    # print(df['Date'])

if __name__ == '__main__':
    main()