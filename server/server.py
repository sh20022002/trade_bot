'''all oop(object orianted programing) uses and there functions'''
from functions import generate_hash
from scraping import exchange_rate
import socket, threading

# add database functions to the client class
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = gethostbyname(gethostname())
port = 8080

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

    
    def chack_open_positions(self, transaction):

        """

        Check if the client has an open position for the transaction's symbol.


        Args:

        - transaction (transaction): The transaction to check.


        Returns:

        - bool: True if the client has an open position, False otherwise.

        """

        for position in self.open_positions:
            #chack all open positions for the transaction symbol

            if position.symbol == transaction.symbol:
                #if the symbol is the same
                if transaction.action == 'buy' & chack_transaction(transaction):
                    #if the transaction is a buy and the client has enough cash

                    open_positions.append(transaction)
                    #add the transaction to the open positions
                    if position.action == 'sale':
                        #if the open position is a sale

                        if position.amount >= transaction.amount:
                            #if the open position amount is greater than the transaction amount

                            position.amount -= transaction.amount
                            #subtract the transaction amount from the open position amount
                            if position.amount == 0:
                                #if the open position amount is zero

                                open_positions.remove(transaction)
                                #remove the open position
                            if position.amount < 0:
                                #if the open position amount is negative

                                open_positions.remove(transaction)
                                #remove the open position
                                transaction.amount = abs(position.amount)
                                #set the transaction amount to the absolute value of the open position amount
                                open_positions.append(transaction)
                                #add the transaction to the open positions
                    return True

                if transaction.action == 'sale':
                    #if the transaction is a sale
                    if position.amount >= transaction.amount:
                        #if the open position amount is greater than the transaction amount

                        position.amount -= transaction.amount
                        #subtract the transaction amount from the open position amount
                        if position.amount == 0:
                            #if the open position amount is zero
                            open_positions.remove(transaction)
                        if position.amount < 0:
                            #if the open position amount is negative
                            open_positions.remove(transaction)
                            transaction.amount = abs(position.amount)
                            open_positions.append(transaction)
                            #add the transaction to the open positions
                    return True   

                position.amount += transaction.amount
                #add the transaction amount to the open position amount
            else:
                #if the symbol is not the same
                if chack_transaction(transaction):
                    #if the client has enough cash
                    open_positions.append(transaction)
                    #add the transaction to the open positions
                    return True
        return False


def initialize():
    # initialize the database
    sp500_compenies = scraping.get_tickers()

    # Index(['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry',

        #    'Headquarters Location', 'Date added', 'CIK', 'Founded']

    compenies = []

    for i in range(2):

        # print(sp500_compenies.index)

        compenies.append(sp500_compenies[1][i])

        compeny = server.compeny(sp500_compenies[2][i], sp500_compenies[1][i])

        compeny.GICS_Sector = sp500_compenies[3][i]

        compeny.GICS_Sub_Industry = sp500_compenies[4][i]

        compeny.Location = sp500_compenies[5][i]

        compeny.CIK = sp500_compenies[6][i]

        compeny.Founded = sp500_compenies[7][i]
        
        database.save_compeny(compeny)

    return compenies
