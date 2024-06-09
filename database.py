'''all database actions'''

import pymongo

import pickle

from api_keys import port, local_host





mycliant = pymongo.MongoClient(local_host)


mydb = mycliant['stocks-consumer']

compenies = mydb['stocks']

mycol2 = mydb['cliant']

models = mydb['models']



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