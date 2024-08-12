'''all database actions'''

import pymongo
import os
import pickle
from functools import wraps
from pymongo import MongoClient

from functions import generate_hash
from pymongo.errors import OperationFailure
from urllib.parse import quote_plus

# Fetch environment variables
db_host = os.getenv('DB_HOST', 'db')
db_port = int(os.getenv('DB_PORT', 27017))
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', 'te13@t$3t')
db_name = os.getenv('DB_NAME', 'SmartTraid')


# parse the URI
db_password = quote_plus(db_password)
db_name = quote_plus(db_name)

# Create the MongoDB client
mongo_uri = f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?authSource=admin"
client = MongoClient(mongo_uri)

mydb = client[db_name]
compenies = mydb['stocks']
users = mydb['cliants']
models = mydb['models']
transactions = mydb['transactions']

#users functions

def add_user(user):
    '''Adds a user to the database.'''
    pass

def remove_from_db(symbol):
    '''Removes a stock from the database based on its symbol.'''
    compenies.delete_one({'symbol': symbol})



def save_compeny(company):
    '''Saves a company's information to the database.'''
    compenies.insert_one({'name': company.compeny_name,
                          'symbol': company.symbol,
                          'Gics_Sector': company.GICS_Sector,
                          'Gics_Sub_Industry': company.GICS_Sub_Industry,
                          'CIK': company.CIK,
                          'Founded': company.Founded,
                          'Location': company.Location,
                          'price': company.price,
                          'sentiment': company.sentiment,
                          'summary': company.summery,})
                        #   'model_1h': company.hourly,
                        #   'model_1d': company.daily,
                        #   'last_update': company.last_update})
    return True

def get_compeny(symbol):
    '''Returns the company information for a given symbol.'''
    compeny = compenies.find_one({'symbol': symbol})
    return compeny

def get_compenies():
    '''Returns all companies in the database.'''
    compenies = compenies.find()
    return compenies
def save_model(symbol, interval, pickled_model, update):
    '''Saves the HMM model for a given stock symbol and interval.'''
    models.insert_one({'interval': interval, 'model': pickled_model,'traind':{'symbol': symbol, 'last_update': update}})
    return True

def save_hmm_model(symbol, interval, pickled_model, update):
    '''Saves the HMM model for a given stock symbol and interval.'''
    models.insert_one({'symbol': symbol, 'interval': interval, 'model': pickled_model, 'last_update': update})
    return True

def get_hmm_model(symbol, interval):
    '''Returns the HMM model for a given stock symbol and interval.'''
    model = models.find_one({'symbol': symbol, 'interval': interval})
    return model

def update_hmm_model(symbol, interval, pickled_model, update):
    '''Updates the hmm model for a given stock symbol and interval.'''
    models.update_one({'symbol': symbol, 'interval': interval, '$set':{ 'model': pickled_model, 'last_update': update}})
    return True

def get_model(interval):
    '''Returns the master model for a given interval.'''
    model = models.find_one({'interval': interval})
    return model

def update_model(symbol, interval, pickled_model, update):
    '''Updates the master model for a given interval.'''
    models.update_one({'interval': interval, '$set': {'model': pickled_model}, 'traind': {'symbol': symbol, '$set': {'last_update': update}}})
    return True

#client functions

def add_client(client):
    '''Adds a client to the database.'''
    users.insert_one({'name': client.name,
                      'username': client.username,
                      'hash': client.hash,
                      'ID': client.ID,
                      'date_of_birth': client.date_of_birth,
                      'age': client.age,
                      'profetion': client.profetion,
                      'bank_account_number': client.bank_account_number,
                      'bank': client.bank,
                      'email': client.email,
                      'phone_number': client.phone_number,
                      'address': client.address,
                      'city': client.city,
                      'country': client.country,
                      'postal_code': client.postal_code,
                      'transactions': client.transactions,
                      'open_positions': client.open_positions,
                      'protfolio': client.protfolio,
                      'cash': client.cash,
                      'stock_value': client.stock_value})
    return True

def get_client(name):
    '''Returns the client information for a given name.'''
    client = users.find_one({' name': name})
    return client

# login functions
def login(username, password):
    '''Logs in a user with the given username and password.'''
    user = users.find_one({'username:': username})
    if user is not None:
        if user['hash'] == generate_hash(password):
            return user
    return None

def mongo_sync(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        # Update MongoDB document after the method call
        self.update_mongo()
        return result
    return wrapper

class MongoSynced:
    def __init__(self, client_id, **kwargs):
        self.client_id = client_id
        self.__dict__.update(kwargs)
        self.update_mongo()

    def update_mongo(self):
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        __name__.update_one({'client_id': self._id}, {'$set': data}, upsert=True) #?? s__name__ class name

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        self.update_mongo()
