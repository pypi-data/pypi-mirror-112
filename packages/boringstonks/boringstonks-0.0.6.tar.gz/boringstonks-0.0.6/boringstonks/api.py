import json
import requests
import pandas 
from flatten_json import flatten
import re

defaultConfig = dict()
defaultConfig['api'] = 'https://boringstonks.com/graphql'
defaultConfig['timeout'] = 50

def handle_req(config, access_token, mod_query, key):
    headers = {'Content-Type': 'application/json', 'Access-Token': access_token}
    x = requests.post(config['api'], data=mod_query, timeout=config['timeout'], headers=headers)
    if x.status_code == 200:
        if 'data' not in x.json():
            print(x.content)
            print("Cannot find data key")
            return

        stocks = x.json()['data'][key]
        if stocks is not None:
            fl = [flatten(d) for d in stocks]
            frame = pandas.DataFrame(fl) 
            return frame
        else:
            return pandas.DataFrame() 
    else:
        print(x.content)
        print("Status code was not 200")
        return

def getStocks(query, access_token, periods = 0, config = defaultConfig):
    mod_query = '{"query": "{ getStocks(periods: %d) { %s } } "}' % (periods, query)
    return handle_req(config, access_token, mod_query, 'getStocks') 

def getStockById(iid, query, access_token, periods = 0, config = defaultConfig):
    mod_query = '{"query": "{ getStockById(id: %d, periods: %d) { %s } } "}' % (iid, periods, query)
    return handle_req(config, access_token, mod_query, 'getStockById') 

def getStockByCIK(cik, query, access_token, periods = 0, config = defaultConfig):
    mod_query = '{"query": "{ getStockByCIK(cik: %s, periods: %d) { %s } } "}' % ("\\\"" + cik + "\\\"", periods, query)
    return handle_req(config, access_token, mod_query, 'getStockByCIK') 

def getStocksByCIKs(ciks, query, access_token, periods = 0, config = defaultConfig):
    cik_str = ','.join(["\\\"" + str(elem) + "\\\"" for elem in ciks])
    mod_query = '{"query": "{ getStocksByCIKs(ciks: [%s], periods: %d) { %s } } "}' % (cik_str, periods, query)
    return handle_req(config, access_token, mod_query, 'getStocksByCIKs') 


def getStocksByTradingSymbol(syms, query, access_token, periods = 0, config = defaultConfig):
    sym_str = ','.join(["\\\"" + str(elem) + "\\\"" for elem in syms])
    mod_query = '{"query": "{ getStocksByTradingSymbol(sym: [%s], periods: %d) { %s } } "}' % (sym_str, periods, query)
    return handle_req(config, access_token, mod_query, 'getStocksByTradingSymbol') 
