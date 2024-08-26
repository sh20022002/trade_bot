import yfinance as yf
from datetime import datetime

def get_stock(stock):
    '''
    Get the recommendation with the largest signal related to the stock.

    Parameters:
    - stock (str): The stock symbol.

    Returns:
    - dict: The recommendation with the largest signal.
    '''
    stock_ticker = yf.Ticker(stock)
    info = stock_ticker.info
    last_dividend_date_timestamp = info.get('lastDividendDate')
    if last_dividend_date_timestamp:
        last_dividend_date = datetime.fromtimestamp(last_dividend_date_timestamp)
        divid = f"{last_dividend_date.strftime('%Y-%m-%d')} :{info.get('lastDividendValue')}"
        print(divid)
    # for key, value in stock_ticker.info.items():
    #     print(key, value)
   

    # print(data)


if __name__ == '__main__':
    get_stock('AAPL')