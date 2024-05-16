import plotly.graph_objects as go


import pandas as pd

def plot_stock(df, stock):

    fig = go.Figure(data=[go.Candlestick(x=df['Date'],

                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])


    fig.show()