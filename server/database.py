'''all database actions'''

import pymongo
import os
import pickle

from functions import generate_hash

local_host = os.getenv('DB_HOST')
port = os.getenv('PORT')

mycliant = pymongo.MongoClient(local_host)
mydb = mycliant['stocks-consumer']
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

def get_hmm_model(symbol, interval):
    '''Returns the HMM model for a given stock symbol and interval.'''
    compeny = compenies.find_one({'symbol': symbol})
    return compeny[f'model_{interval}']

def save_compeny(company):
    '''Saves a company's information to the database.'''
    compenies.insert_one({'name': company.name,
                          'symbol': company.symbol,
                          'Gics_Sector': company.Gics_Sector,
                          'Gics_Sub_Industry': company.Gics_Sub_Industry,
                          'CIK': company.CIK,
                          'Founded': company.Founded,
                          'Location': company.Location,
                          'price': company.price,
                          'score': company.score,
                          'sentiment': company.sentiment,
                          'summary': company.summary,
                          'model_1h': company.hourly,
                          'model_1d': company.daily,
                          'last_update': company.last_update})
    return True

def get_compeny(symbol):
    '''Returns the company information for a given symbol.'''
    compeny = mycol2.find_one({'symbol': symbol})
    return compeny

def get_compenies():
    '''Returns all companies in the database.'''
    compenies = mycol2.find()
    return compenies

def update_model(symbol, interval, pickled_model):
    '''Updates the model for a given stock symbol and interval.'''
    mycol2.update_one({'symbol': symbol, 'interval': interval}, {'$set': {'model': pickled_model}})
    return True

def get_master_model(interval):
    '''Returns the master model for a given interval.'''
    model = models.find_one({'interval': interval})
    return model['model']

def update_master_model(interval, pickled_model):
    '''Updates the master model for a given interval.'''
    models.update_one({'interval': interval}, {'$set': {'model': pickled_model}})
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
    if user['hash'] == generate_hash(password):
        return user
    else:
        return None