'''all oop(object orianted programing) uses and there functions'''
from functions import generate_hash
from scraping import exchange_rate

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
