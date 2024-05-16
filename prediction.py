'''uses the model to predict stock vulability'''
import plots
import scraping
from functions import add_all, calculate_rsi
import pandas as pd

def predict_trend(stock):
    df = scraping.get_stock_data(stock, interval='1h')
    df = add_all(df)
    
    return df

def rsi(stock):
    df = scraping.get_stock_data(stock)
    si = calculate_rsi(df)
    print(si)


def main():
    stock = 'AAPL'
    # rsi(stock)
    df = predict_trend(stock)
    print(df.columns)
    plots.plot_stock(df, stock)
    

if __name__ == '__main__':
    main()