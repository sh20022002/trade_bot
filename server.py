'''all oop(object orianted programing) uses and there functions'''


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

    def __init__(self, first_name, last_name, ID, date_of_birth, profetion, cash, bank_account_number, bank, email, phone_number, address, city, country, postal_code):

        self.name = first_name + last_name
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

            self.open_positions.append(buy)
        

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
    