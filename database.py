'''all database actions'''
import pymongo

local_host = '' '''url path'''

mycliant = pymongo.MongoClient(local_host)

mydb = mycliant['stocks-consumer']

mycol = mydb['stocks']
mycol2 = mydb['cliant']

def insert_stock(name, symbol):
    '''Inserts a single stock into the database.'''
    x = '{name' + f':{name},' + 'symbol' + f':{symbol}' + '}'
    data = mycol.insert_one(x)

def insert_stocks(names, symbols):
    '''Inserts multiple stocks into the database.'''
    data = []
    for name, symbol in zip(names, symbols):
        x = '{name' + f':{name},' + 'symbol' + f':{symbol}' + '}'
        data.insert(x)
    data = mycol.insert_many(x)

def find_s(symbol):
    '''Finds a stock in the database based on its symbol.'''
    mycol.find_one(symbol)

def find_stock(symbol):
    '''Returns all stock data and initializes it in a company object.'''
    pass

def remove_from_db(symbol):
    '''Removes a stock from the database based on its symbol.'''
    mycol.delete_one({'symbol': symbol})

def get_hmm_model(symbol, interval):
    pass

def save_compeny(company):
    pass

def get_compeny(symbol):
    pass

def update_model(symbol, date):
    pass

def get_master_model(symbol, interval):
    pass

def update_master_model():
    pass