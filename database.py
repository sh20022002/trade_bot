'''all database actions'''

import pymongo

import pickle

from api_keys import port, local_host





mycliant = pymongo.MongoClient(local_host)


mydb = mycliant['stocks-consumer']

compenies = mydb['stocks']

users = mydb['cliants']

models = mydb['models']

transactions = mydb['transactions']

#users functions

def add_user(user):
    pass

def remove_from_db(symbol):

    '''Removes a stock from the database based on its symbol.'''
    compenies.delete_one({'symbol': symbol})


def get_hmm_model(symbol, interval):
    compeny = compenies.find_one({'symbol': symbol})
    return compeny[f'model_{interval}']


def save_compeny(company):

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

                        'model_1h': company.hourly, #

                        'model_1d':company.daily, #
                        
                        'last_update': company.last_update})

    return True


def get_compeny(symbol):

    compeny = mycol2.find_one({'symbol': symbol})
    return compeny


def update_model(symbol, interval, pickled_model):

    mycol2.update_one({'symbol': symbol, 'interval': interval}, {'$set': {'model': pickled_model}})

    return True


def get_master_model(interval):

    model = models.find_one({'interval': interval}) ## needs to be tested

    return model['model']


def update_master_model(interval, pickled_model):

    models.update_one({'interval': interval}, {'$set': {'model': pickled_model}})

    return True

#client functions

def add_client(client):

    users.insert_one({'name': client.name,
                     'username': client.username,
                     'hash': client.hash, ## needs to be added
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

    client = users.find_one({' name': name})
    return client