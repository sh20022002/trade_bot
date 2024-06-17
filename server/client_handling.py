'''all oop(object orianted programing) uses and there functions'''

from functions import generate_hash

from scraping import exchange_rate, current_stock_price




# add database functions to the client class



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


    def __init__(self, first_name, last_name, password, ID, date_of_birth, profetion, cash, bank_account_number, bank, email, phone_number, address, city, country, postal_code):


        self.name = first_name + last_name

        self.username = self.name + str(ID)

        self.hash = generate_hash(password)

        self.ID = ID

        self.date_of_birth = date_of_birth

        self.profetion = profetion

        self.bank_account_number = bank_account_number

        self.bank = bank

        self.email = email

        self.phone_number = phone_number

        self.address = address

        self.city = city

        self.country = country

        self.postal_code = postal_code

        self.transactions = []

        self.open_positions = []

        self.protfolio = []

        self.cash = cash

        self.stock_value = 0

    


    


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





    def chack_transaction(self, transaction):
        """
        Check if the client has enough cash to make a transaction.

        Args:
        - transaction (transaction): The transaction to check.

        Returns:
        - bool: True if the client has enough cash, False otherwise.
        """
        if transaction.total_price <= self.cash:
            return True
        else:
            return False

    

    def make_transaction(self, transaction):
        pass




    def close_position(self, position):
        pass

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

        amount_to_sell = round(position.amount * minimizeby)
        if amount_to_sell > 0:
            if position.action == 'buy':
                if authorize(amount_to_sell * current_stock_price(position.symbol)):
                    self.sale(position.symbol, amount_to_sell)
            else:
                if authorize(amount_to_sell * current_stock_price(position.symbol)):
                    self.buy(position.symbol, amount_to_sell)
        