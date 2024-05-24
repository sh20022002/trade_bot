'''all oop(object orianted programing) uses and there functions'''
from scraping import get_stock_sum, current_stock_price
from functions import summery ,add_all , calculate_hourly_returns
from plots import plot_stock
from database import find_s, remove_from_db, insert_stock
from training import train_hmm
from prediction import predict_next_state_and_probabilities, stock_and_tecnical

class client():
    """
    Represents a client in a trading system.

    Attributes:
    - name (str): The name of the client.
    - age (int): The age of the client.
    - profession (str): The profession of the client.
    - cash (float): The amount of cash the client has.
    - transactions (list): A list of completed transactions made by the client.
    - open_transactions (list): A list of open transactions made by the client.
    - portfolio (list): A list of symbols in the client's portfolio.
    - stock_value (float): The total value of stocks owned by the client.
    """

    def __init__(self, name, age, profession, cash):
        self.name = name
        self.age = age
        self.profession = profession
        self.cash = cash
        self.transactions = []
        self.open_transactions = []
        self.portfolio = []
        self.stock_value = 0

    # Rest of the code...
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
        """
        Perform a stock transaction for the client.

        Args:
        - symbol (str): The symbol of the stock.
        - amount (int): The amount of stock to buy or sell.
        - action (str): The action to perform, either 'buy' or 'sale'.
        - strategy (str): The trading strategy to use.
        - target_price (float, optional): The target price for the transaction.

        Returns:
        - str: A string representing the transaction details.
        """
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
        """
        Get a string representation of the client's transactions.

        Returns:
        - str: A string representing the client's transactions.
        """
        body = 'transaction:'
        space = len(body)
        body += 'action   compeny   price   amount   val\n'
        for tran in self.transaction:
            body += ' '*space + f'{tran.action}---{tran.symbol}---{tran.price}---{tran.amount}   {tran.sum_val} \n'
        return body

    
    def protfolio__str__(self):
        """
        Get a string representation of the client's portfolio.

        Returns:
        - str: A string representing the client's portfolio.
        """
        body = 'protfolio:' +'\n' + '---'
        for symbol in self.protfolio:
            body += f'{symbol} \n'
        return body
            
    def open_transactions__str__(self):
        """
        Get a string representation of the client's open transactions.

        Returns:
        - str: A string representing the client's open transactions.
        """
        body = 'open transaction:'
        space = len(body)
        body += 'action   compeny   price   amount   val   current price   precantage\n'
        for tran in self.transaction:
            body += ' '*space + f'{tran.action}---{tran.symbol}---{tran.price}---{tran.amount}---{tran.sum_val}---{current_stock_price(tran.symbol)} \n'
        return body

    def deposit(self, amount):
        """
        Deposit cash into the client's account.

        Args:
        - amount (float): The amount of cash to deposit.

        Returns:
        - str: A string representing the deposit details.
        """
        self.cash += amount
        return f'deposited: {amount}---cash in account: {self.cash}'
    
    def withdraw(self, amount):
        """
        Withdraw cash from the client's account.

        Args:
        - amount (float): The amount of cash to withdraw.

        Returns:
        - str: A string representing the withdrawal details.
        """
        if self.cash >= amount:
            self.cash -= amount
            return f'withdraw: {amount}---cash in account: {self.cash}'
        else:
            return 'not sefichant cash in account!'
    



class compeny:
    def __init__(self, compeny_name, symbol):
        self.compeny_name = compeny_name
        self.symbol = symbol
        self.Security = None
        self.GICS_Sector = None
        self.GICS_Sub_Industry = None
        self.CIK = None
        self.Founded = None
        self.Location = None
        self.interval = '1h'
        self.summery = get_stock_sum('short\long-none\sma\50\100\200-none\pricer-none\price-prediction')
        self.price = current_stock_price(self.symbol)
        self.last_price = None
        self.score = None #predict_vall()
        self.sentiment = None
        self.hmm = None
        
        
    
    @property
    def get_df(self, DAYS=365):
        """
        Get the stock data for the company.

        Args:
        - DAYS (int, optional): The number of days of data to retrieve.

        Returns:
        - DataFrame: The stock data for the company.
        """
        df = stock_and_tecnical(self.symbol, interval=self.interval)
        return df


    @property
    def show(self):
        """
        Show the stock data for the company.
        """
        plot_stock(self.get_df, self.compeny_name, show='all', interval=self.interval)



    def probability_of_returns(self):
        """
        Calculate the probability of future stock returns using the HMM model.
        """
        # needs a function to refit the hmm model

        df = self.get_df
        df = add_all(df)
        current_return = df['Close'][0] - df['Close'][1]
        if(self.hmm == None):
            self.hmm = train_hmm(self.symbol, df)

        state, probability = predict_next_state_and_probabilities(self.hmm, current_return)

        prediction = None
        

# for now no use for database because of the small amount data and the need for it to be updated frquantly
# if will be used for more then one costomer will need a database and methods to update all data frequantly 
# and there will be an advange for bigger usege doo to the better accessing times and aficcentce to run and grow
# --needs an updated aprouch for scallability

    
    def add_stock(self, compeny_name, symbol, summery):
        """
        Add a stock to the database.

        Args:
        - compeny_name (str): The name of the company.
        - symbol (str): The symbol of the stock.
        - summery (str): The summary of the stock.

        Returns:
        - str: A string representing the result of adding the stock.
        """
        stock = compeny(self, compeny_name, symbol, summery)
        insert_stock(compeny_name, symbol)
        return f'added {compeny_name}.'
    
    def del_stock(self):
        """
        Remove the stock from the database.

        Returns:
        - str: A string representing the result of removing the stock.
        """
        ans = find_s(self.symbol)
        if ans:
            r = remove_from_db(self.symbol)
            if r:
                return f'{self.compeny_name} removed from database!'
        else:
            return f'{self.compeny_name} not found in tatabase'


  
    