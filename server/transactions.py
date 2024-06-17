from scraping import get_exchange_time, current_stock_price
import strategy as st
class transaction:
    """
    Represents a transaction in the trading system.

    Attributes:
        action (str): The action of the transaction (buy or sale).
        symbol (str): The symbol of the stock being traded.
        value (float): The current stock price.
        amount (int): The amount of stock being traded.
        total_price (float): The total price of the transaction.
        date (datetime): The date and time of the transaction.
    """

    def __init__(self):
        self.action = None
        self.symbol = None
        self.compeny = database.get_compeny(self.symbol)
        self.value = current_stock_price(self.symbol)
        self.amount = 0
        self.total_price = value * amount
        self.date = get_exchange_time()
        self.strategy = st.optimaize(self.action, self.symbol, self.value, self.amount, self.total_price, self.date)

    def __str__(self):
        return f'{self.action}: {self.symbol}---price: {self.value}---{self.amount}---{self.total_price}---{self.date}'

    def buy(self, symbol, amount):
        self.action = 'buy'
        self.symbol = symbol
        self.amount = amount
        self.value = current_stock_price(self.symbol)
        self.total_price = self.value * amount
        self.date = get_exchange_time()
        

    def sale(self, symbol, amount):
        self.action = 'sale'
        self.symbol = symbol
        self.amount = amount
        self.value = current_stock_price(self.symbol)
        self.total_price = self.value * amount
        self.date = get_exchange_time()
        
