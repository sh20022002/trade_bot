'''all oop(object orianted programing) uses and there functions'''

from functions import generate_hash

from scraping import get_exchange_rate, current_stock_price

from database import MongoSynced
import database, json


# add database functions to the client class



class client(MongoSynced):


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


    def __init__(self, client):
        # super().__init__(transactions, open_positions, protfolio, cash, stock_value)
    
        client = json.loads(client)
    
        self.name = client['first_name'] + client['last_name']
    
        self.username = self.name + str(client['ID'])
    
        self.hash = generate_hash(client['password'])
                    
    
        self.ID = client['ID']
    
        self.date_of_birth = client['date_of_birth']
    
        self.profetion = client['profetion']
    
        self.bank_account_number = client['bank_account_number']
    
        self.bank = client['bank']
    
        self.email = client['email']
    
        self.phone_number = client['phone_number']
    
        self.address = client['address']
    
        self.city = client['city']
    
        self.country = client['country']
    
        self.postal_code = client['postal_code']
    
        self.transactions = []
    
        self.open_positions = []
    
        self.protfolio = []
    
        self.cash = 0
    
        self.stock_value = 0

    

    def initialize(self, client):
        try:
            self.ID = client['ID']
            self.date_of_birth = client['date_of_birth']
            self.profession = client['profession']
            self.bank_account_number = client['bank_account_number']
            self.bank = client['bank']
            self.email = client['email']
            self.phone_number = client['phone_number']
            self.address = client['address']
            self.city = client['city']
            self.country = client['country']
            self.postal_code = client['postal_code']
            self.transactions = []
            self.open_positions = []
            self.portfolio = []
            self.cash = 0
            return True
        except KeyError as e:
            print(f"Missing key: {e}")
            return False


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
            

    

    @database.mongo_sync
    def deposit(self, amount, currency='USD'):


        """


        Deposit cash into the client's account.



        Args:


        - amount (float): The amount of cash to deposit.



        Returns:


        - str: A string representing the deposit details.


        """

        if currency != 'USD':

            exchange_rate = get_exchange_rate(currency, 'USD')

            amount = amount * exchange_rate

        self.cash += amount


        return f'deposited: {amount}---cash in account: {self.cash}'
    

    @database.mongo_sync
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

            if currency != 'USD':

                exchange_rate = get_exchange_rate(currency, 'USD')

                amount = amount * exchange_rate


            return f'withdraw: {amount}---cash in account: {self.cash} in {currency}'
        else:


            return 'not sefichant cash in account!'


    @database.mongo_sync
    def buy(self, symbol, amount):
        """
        Buy a specified amount of stocks.

        Args:
        - symbol (str): The symbol of the stock to buy.
        - amount (int): The amount of stock to buy.

        Returns:
        - None
        """
        if self.autharaize(transaction.buy(symbol, amount)):
            for position in self.open_positions:
                if position.symbol == symbol:
                    break
            try:
                position.add_to_position(amount)
            except:
                self.open_positions.append(transaction.buy(symbol, amount))
                    
            self.cash -= transaction.total_price
            self.transactions.append(transaction.buy(symbol, amount))
            self.protfolio.append(symbol)
            self.stock_value += current_stock_price(symbol) * amount
            return f'buy: {amount} {symbol}---cash in account: {self.cash}'
        else:
            return 'not sefichant cash in account!'

    @database.mongo_sync
    def sell(self, symbol, amount):
        """
        Buy a specified amount of stocks.

        Args:
        - symbol (str): The symbol of the stock to buy.
        - amount (int): The amount of stock to buy.

        Returns:
        - None
        """
        if self.autharaize(transaction.sell(symbol, amount)):
            # to minimize risk takes shorts only if threre is sefichant cash in account to cover the short 
            
            for position in self.open_positions:
                if position.symbol == symbol:
                    pos = position
                    break

            if pos:
                self.minimize(pos, amount)
                self.protfolio.remove(symbol) #???
                self.open_positions.remove(pos) #???
                self.stock_value -= current_stock_price(symbol) * amount
            else:
                self.open_positions.append(transaction.sell(symbol, amount))
                self.stock_value += current_stock_price(symbol) * amount
                    
            self.cash += transaction.total_price
            self.transactions.append(transaction.sell(symbol, amount))
            
            
            return f'buy: {amount} {symbol}---cash in account: {self.cash}'
        else:
            return 'not sefichant cash in account!'

    




    def autharaize(self, total_price):
        if total_price <= self.cash:
            return True
        else:
            return False


    def minimize(self, position, minimizeby):
        """
        Minimizes the position by selling or buying a specified amount of stocks.

        Args:
            position (Position): The position to be minimized.
            minimizeby (float): The percentage by which to minimize the position.

        Returns:
            None

        Raises:
            None
        """

        amount_to_sell = round(position.amount *(minimizeby/100)) 
        if amount_to_sell > 0:
            if position.action == 'buy':
                if authorize(amount_to_sell * current_stock_price(position.symbol)):
                    self.sale(position.symbol, amount_to_sell)
            else:
                if authorize(amount_to_sell * current_stock_price(position.symbol)):
                    self.buy(position.symbol, amount_to_sell)
        


    def add_closed_position(self):
        """
        adds closed postion to the database with all transaction details
        and id and the return on the investment
        """
        pass