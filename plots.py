import plotly.graph_objects as go
from datetime import datetime, timedelta


import pandas as pd

def plot_stock(df, stock, show='no'):

    df['Datetime'] = pd.to_datetime(df['Datetime'])

# Create a boolean mask for the dates you want to keep
    mask = ~(((df['Datetime'].dt.month == 12) & (df['Datetime'].dt.day.isin([24, 25]))) |
            ((df['Datetime'].dt.month == 2) & (df['Datetime'].dt.day == 19)))

# Apply the mask to the DataFrame
    df = df[mask]

    fig = go.Figure()
    
    fig.add_trace(go.Candlestick(x=df['Datetime'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name=stock))
    if(show == 'all'):
        for column in ['moa-50', 'moa-100', 'moa-200', 'EMA', 'TR', 'DMplus', 'DMminus', 'ATR', 'DMplus_smoothed', 'DMminus_smoothed', 'DIplus', 'DIminus', 'DX', 'ADX']:
            fig.add_trace(go.Scatter(x=df['Datetime'], y=df[column], name=column))

    fig.update_xaxes(
                    rangeslider_visible=True,
                    rangebreaks=[
            # : Below values are bound (not single values), ie. hide x to y
                                dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
                                dict(bounds=[16, 9.5], pattern="hour")]) # hide hours outside of 9.30am-4pm
                                
    
    fig.show()