from scraping import get_exchange_time, current_stock_price

class transaction:
    def __init__(self):
        self.action = None #buy or sale
        self.symbol = None
        self.value = current_stock_price(self.symbol)
        self.amount = 0
        self.total_price = value * amount
        self.date = get_exchange_time()

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
        
