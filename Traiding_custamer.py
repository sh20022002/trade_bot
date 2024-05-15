'''all oop(object orianted programing) uses and there functions'''
from scraping import get_stock_news, current_stock_price, get_stock_data
from functions import summery
from plots import plot_stock
from database import find_s, remove_from_db, insert_stock

class client():
    def __init__(self, name, age, profetion, cash):
        self.name = name
        self.age = age
        self.profetion = profetion
        self.transactions = []
        self.open_transactions = []
        self.protfolio = []
        self.cash = cash
        self.stock_value = 0

    
    
    def stock(self, symbol, amount, action, strategy, target_price=None):
        if action == 'sale':
            buy = transaction(symbol, amount, strategy, buy=False, target_price=None)
        else:
            buy = transaction(symbol, amount, strategy, buy, target_price=None)
        self.transactions.append(buy)
        resolve, tamount, tbuy = self.open_resolve(buy)
        if resolve:
            buy = transaction(symbol, tamount, strategy, tbuy, target_price=None)
            self.open_transactions.append(buy)
        
        self.protfolio.append(buy.symbol)
        if action =='sale':
            self.cash -= buy.sum_val
            self.stock_value += buy.amount * buy.price_in_sale
        else:
            self.cash += buy.sum_val
            # change price in sale to current price
            self.stock_value += buy.amount * buy.price_in_sale
        strategy_sum = summery(strategy)
        if target_price != None:
            # adds the target price if there is
            return f'{action}: {buy.symbol}---price: {buy.price_in_sale}---{strategy_sum}---target: {target_price}'
        else:
            return f'{action}: {buy.symbol}---price: {buy.price_in_sale}---{strategy_sum}'

    def transactions__str__(self):
        body = 'transaction:'
        space = len(body)
        body += 'action   compeny   price   amount   val\n'
        for tran in self.transaction:
            body += ' '*space + f'{tran.action}---{tran.symbol}---{tran.price}---{tran.amount}   {tran.sum_val} \n'
        return body

    
    def protfolio__str__(self):
        # returns all symbols in protfolio
        body = 'protfolio:' +'\n' + '---'
        for symbol in self.protfolio:
            body += f'{symbol} \n'
        return body
            
    def open_transactions__str__(self):
        body = 'open transaction:'
        space = len(body)
        body += 'action   compeny   price   amount   val   current price   precantage\n'
        for tran in self.transaction:
            body += ' '*space + f'{tran.action}---{tran.symbol}---{tran.price}---{tran.amount}---{tran.sum_val}---{current_stock_price(tran.symbol)} \n'
        return body

    def deposit(self, amount):
        self.cash += amount
        return f'deposited: {amount}---cash in account: {self.cash}'
    
    def withdraw(self, amount):
        if self.cash >= amount:
            self.cash -= amount
            return f'withdraw: {amount}---cash in account: {self.cash}'
        else:
            return 'not sefichant cash in account!'
    



class compeny:
    def __init__(self, compeny_name, symbol, summery):
        self.compeny_name = compeny_name
        self.symbol = symbol
        self.summery = summery
        self.price = None
        self.last_price = None
        self.score = predict_vall()
        # self.news = get_stock_news()
        self.show = plot_stock(self.compeny_name)
    
    @property
    def get_df(self, DAYS=100):
        return get_stock_data(self.symbol, DAYS)
        

    
    def add_stock(self, compeny_name, symbol, summery):
        stock = compeny(self, compeny_name, symbol, summery)
        insert_stock(compeny_name, symbol)
        return f'added {compeny_name}.'
    
    def del_stock(self):
        ans = find_s(self.symbol)
        if ans:
            r = remove_from_db(self.symbol)
            if r:
                return f'{self.compeny_name} removed from database!'
        else:
            return f'{self.compeny_name} not found in tatabase'


  
    