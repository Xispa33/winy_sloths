#!/usr/bin/python3
# -*- coding: utf-8 -*-

from binance.client import Client
import binance
from constants import *
import os
import sys
from time import *
from datetime import *
import traceback

def I__CLIENT(api_key, api_secret_key):
    """
    Name : I__CLIENT()
    
    Parameters : 
                  api_key : str
                    api key used to connect to Binance server
        
                  api_secret_key : str
                    api secret key used to connect to Binance server
    
    Description : This function pings Binance servers with the API key
                  provided in parameters.
    """
    FUNCTION = "I__CLIENT"
    err_cpt = 0
    ret = 1
    client = 1

    while (err_cpt < MAX_RETRY*4) and (ret == 1):
        try:
            client = Client(api_key, api_secret_key)
            ret = 0
        except:
            ret = 1
            err_cpt += 1
            print(FUNCTION)
            print("DATE : {}".format(str(datetime.now())))
            print(sys.exc_info())
            sleep(1)
    
    return client

def I__FUTURES_ACCOUNT_TRADES(client, symbol):
    """
    Name : I__FUTURES_ACCOUNT_TRADES()
    
    Parameters : 
                  client : binance.client
                    Client used to connect to Binance server

                  symbol : str
                    Currency traded
    
    Description : Gets a symbol's trade history of a futures account. 
                  Client contains the API key credentials allowing to
                  connect to Binance server
                  If this function fails MAX_RETRY times, an error is
                  returned
    """
    FUNCTION = "I__FUTURES_ACCOUNT_TRADES"
    err_cpt = 0
    ret = 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            ret = client.futures_position_information(symbol=symbol, timestamp=client.futures_time())
        except:
            ret = 1
            err_cpt += 1
            print(FUNCTION)
            print("DATE : {}".format(str(datetime.now())))
            print("Binance return was not good for the {}th time ! \n".format(err_cpt))
    return ret

def I__SPOT_ACCOUNT_TRADES(client, symbol):
    """
    Name : I__SPOT_ACCOUNT_TRADES()
    
    Parameters : 
                  client : binance.client
                    Client used to connect to Binance server

                  symbol : str
                    Currency traded 
    
    Description : Gets a symbol's trade history of a SPOT account. 
                  Client contains the API key credentials allowing 
                  to connect to Binance server
                  If this function fails MAX_RETRY times, an error 
                  is returned
    """
    FUNCTION = "I__SPOT_ACCOUNT_TRADES"
    err_cpt = 0
    ret = 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            ret = client.get_all_orders(symbol=symbol, limit='1')
        except:
            ret = 1
            err_cpt += 1
            print(FUNCTION)
            print("DATE : {}".format(str(datetime.now())))
            print("Binance return was not good for the {}th time ! \n".format(err_cpt))
    return ret

def I__GET_ACCOUNT_HISTORY(client, account_type, symbol):
    """
    Name : I__GET_ACCOUNT_HISTORY()
    
    Parameters : 
                  client : binance.client
                    Client used to connect to Binance server

                  account_type : str
                    Type of account, either 'SPOT' or 'FUTURES'

                  symbol : str
                    Currency traded
    
    Description : Gets a symbol's trade history, depending on the 
                  account_type. 
                  Client contains the API key credentials allowing 
                  to connect to Binance server
    """
    if (account_type == SPOT):
        ret = I__SPOT_ACCOUNT_TRADES(client, symbol)
    elif (account_type == FUTURES):
        ret = I__FUTURES_ACCOUNT_TRADES(client, symbol)
    else:
        ret = 1
    
    return ret

def I__CLOSE_LONG_SPOT(client, symbol):
    """
    Name : I__CLOSE_LONG_SPOT()
    
    Parameters : 
                  client : binance.client
                    Client used to connect to Binance server

                  symbol : str
                    Currency traded
    
    Description : Function closing an open trade on a SPOT account.
                  If this function fails MAX_RETRY times, an error is 
                  returned
    """
    FUNCTION = "I__CLOSE_LONG_SPOT"
    err_cpt = 0
    ret = 1

    if (symbol == BTCUSDT):
        curr_asset = BTC
    elif (symbol == ETHUSDT):
        curr_asset = ETH
    else:
        return 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            price = client.get_avg_price(symbol=symbol)[PRICE]
            asset = round(float(client.get_asset_balance(asset=curr_asset)[FREE])*float(price) - 0.05,1)
            client.create_order(symbol=symbol, side=SELL, type=MARKET, quoteOrderQty=asset, timestamp=client.get_server_time())
            ret = 0
        except:
            ret = 1
            err_cpt += 1
            print(FUNCTION)
            print(sys.exc_info())
            sleep(0.5)
    
    return ret

def I__CLOSE_LONG_FUTURES(client, symbol):
    """
    Name : I__CLOSE_LONG_FUTURES()
    
    Parameters : 
                  client : binance.client
                    Client used to connect to Binance server
                  
                  symbol : str
                    Currency traded
    
    Description : Function closing an open trade on a FUTURES account.
                  If this function fails MAX_RETRY times, an error is
                  returned
    """
    FUNCTION = "I__CLOSE_LONG_FUTURES"
    err_cpt = 0
    ret = 1

    precision = 0

    if (symbol == BTCUSDT):
        precision = 3
    elif (symbol == ETHUSDT):
        precision = 2
    else:
        return 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            last_trade = I__FUTURES_ACCOUNT_TRADES(client, symbol)

            for dic in last_trade:
                if dic[POSITION_SIDE] == LONG:
                    ret = dic

            client.futures_create_order(symbol=symbol, positionside=LONG, side=SELL, \
                                        type=MARKET, quantity=round(float(ret[POSITION_AMT]), precision), \
                                        timestamp=client.futures_time())
            ret = 0
        except:
            ret = 1
            err_cpt += 1
            print(FUNCTION)
            print(sys.exc_info())
            sleep(0.5)
    
    return ret

def I__CLOSE_LONG(client, master_api):
    """
    Name : I__CLOSE_LONG()
    
    Parameters : 
                  client : binance.client
                    Client used to connect to Binance server

                  master_api : ApiKeyMaster
                    Binance account handled by EC
    
    Description : Function closing an open trade depending on 
                  the accounts type (SPOT/FUTURES).
                  Client contains the API key credentials allowing
                  to connect to Binance server.
    """
    if (master_api.account_type == SPOT):
        ret = I__CLOSE_LONG_SPOT(client, master_api.symbol)
    elif (master_api.account_type == FUTURES):
        ret = I__CLOSE_LONG_FUTURES(client, master_api.symbol)
    else:
        ret = 1
        
    return ret

def I__OPEN_LONG_SPOT(client, symbol):
    """
    Name : I__OPEN_LONG_SPOT()
    
    Parameters : 
                  client : binance.client
                    Client used to connect to Binance server
                  
                  symbol : str
                    Currency traded
    
    Description : Function opening a trade on a SPOT account
                  If this function fails MAX_RETRY times, an error 
                  is returned
    """
    FUNCTION = "I__OPEN_LONG_SPOT"
    err_cpt = 0
    ret = 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            usdt_asset = client.get_asset_balance(asset=USDT)[FREE]
            asset_round=round(float(usdt_asset)-0.05,1)

            client.create_order(symbol=symbol, side=BUY, type=MARKET, quoteOrderQty=asset_round, timestamp=client.get_server_time())
            ret = 0
        except:
            ret = 1
            err_cpt += 1
            print(FUNCTION)
            print(sys.exc_info())
            sleep(0.5)
    
    return ret

def I__OPEN_LONG_FUTURES(client, symbol, leverage, engaged_balance, entryPrice):
    """
    Name : I__OPEN_LONG_FUTURES()
    
    Parameters : 
                  client : binance.client
                    Client used to connect to Binance server
                  
                  symbol : str
                    Currency traded
                  
                  leverage : str
                    Trade's leverage. This parameter has to be a string 
                    of an integer
                  
                  engaged_balance : float
                    Rate of the wallet engaged on the trade
                  
                  entryPrice : float
                    Current price of the currency
    
    Description : Function opening a trade on a FUTURES account
                  If this function fails MAX_RETRY times, an error 
                  is returned
    """
    FUNCTION = "I__OPEN_LONG_FUTURES"
    err_cpt = 0
    ret = 1

    precision = 0

    if (symbol == BTCUSDT):
        precision = 3
    elif (symbol == ETHUSDT):
        precision = 2
    else:
        return 1
    
    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            ret = client.futures_position_information(symbol=symbol, timestamp=client.futures_time())
            if (len(ret) == 1):
                client.futures_change_position_mode(dualSidePosition=TRUE,timestamp=client.futures_time())
            
            client.futures_change_leverage(symbol=symbol,leverage=leverage,timestamp=client.futures_time())

            bin_ret=client.futures_account_balance(timestamp=client.futures_time())

            for dic in bin_ret:
                if dic[ASSET] == USDT:
                    ret = dic

            balance=ret[WITHDRAW_AVAILABLE]

            quantity=round(((float(balance)*engaged_balance/entryPrice)- (5*10**(-precision-1))),precision)
 
            if (quantity < (1*10**(-precision))):
                quantity = 1*10**(-precision)
            
            client.futures_create_order(symbol=symbol, side=BUY, positionSide=LONG, type=MARKET, quantity=quantity ,timestamp=client.futures_time())

            ret = 0
        except:
            ret = 1
            err_cpt += 1
            print(FUNCTION)
            print(sys.exc_info())
            sleep(0.5)
    
    return ret

def I__OPEN_LONG(client, master_api):
    """
    Name : I__OPEN_LONG()
    
    Parameters : 
                  client : binance.client
                    Client used to connect to Binance server
                  
                  master_api : ApiKeyMaster
                    Binance account handled by EC
    
    Description : Function opening a trade depending on 
                  the accounts type (SPOT/FUTURES).
                  Client contains the API key credentials allowing
                  to connect to Binance server.
    """
    if (master_api.account_type == SPOT):
        ret = I__OPEN_LONG_SPOT(client, master_api.symbol)
    elif (master_api.account_type == FUTURES):
        ret = I__OPEN_LONG_FUTURES(client, master_api.symbol, master_api.leverage, \
                                   master_api.engaged_balance, master_api.entryPrice)
    else:
        ret = 1

    return ret

def I__GET_FUTURES_ACCOUNT_BALANCE(client):
    """
    Name : I__GET_FUTURES_ACCOUNT_BALANCE()
    
    Parameters : 
                  client : binance.client
                    Client used to connect to Binance server
    
    Description : Function returning a futures account information
                  If this function fails MAX_RETRY times, an error is 
                  returned
    """
    err_cpt = 0
    ret = 1

    while (err_cpt < MAX_RETRY*5) and (ret == 1):
        try:
            bin_ret = client.futures_account_balance(timestamp=client.futures_time())
            for dic in bin_ret:
                if dic[ASSET] == USDT:
                    ret = dic
        except:
            ret = 1
            err_cpt += 1
            print("futures_account_balance() return failed\n")
            sleep(0.5)
    return ret

def I__CLOSE_SHORT(client, symbol, leverage):
    """
    Name : I__CLOSE_SHORT()
    
    Parameters : 
                  client : binance.client
                    Client used to connect to Binance server

                  symbol : str
                    Currency traded

                  leverage : str
                    Leverage
    
    Description : Function closing a short position for a FUTURES account
                  If this function fails MAX_RETRY times, an error is 
                  returned
    """
    FUNCTION = "I__CLOSE_SHORT"
    err_cpt = 0
    ret = 1
    precision = 0

    if (symbol == BTCUSDT):
        precision = 3
    elif (symbol == ETHUSDT):
        precision = 2
    else:
        return 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            last_trade = I__FUTURES_ACCOUNT_TRADES(client, symbol)

            for dic in last_trade:
                if dic[POSITION_SIDE] == SHORT:
                    ret = dic
            
            quantity = round(abs(float(ret[POSITION_AMT])), precision)
            client.futures_create_order(symbol=symbol, positionside=SHORT, side=BUY, \
                                        type=MARKET, quantity=quantity, \
                                        timestamp=client.futures_time())
            ret = 0
        except:
            ret = 1
            err_cpt += 1
            print(FUNCTION)
            print(sys.exc_info())
            sleep(0.5)
    
    return ret
    
def I__OPEN_SHORT(client, symbol, leverage, engaged_balance, entryPrice):
    """
    Name : I__OPEN_SHORT()
    
    Parameters : 
                  client : binance.client
                    Client used to connect to Binance server

                  symbol : str
                    Currency traded

                  leverage : str
                    Trade's leverage. This parameter has to be a string 
                    of an integer

                  engaged_balance : float
                    Rate of the wallet engaged on the trade

                  entryPrice : float
                    Current price of the currency
    
    Description : Function opening a short position for a FUTURES account
                  If this function fails MAX_RETRY times, an error is 
                  returned
    """
    FUNCTION = "I__OPEN_SHORT"
    err_cpt = 0
    ret = 1

    precision = 0

    if (symbol == BTCUSDT):
        precision = 3
    elif (symbol == ETHUSDT):
        precision = 2
    else:
        return 1

    while (err_cpt < MAX_RETRY) and (ret == 1):
        try:
            ret = client.futures_position_information(symbol=symbol, timestamp=client.futures_time())
            if (len(ret) == 1):
                client.futures_change_position_mode(dualSidePosition=TRUE,timestamp=client.futures_time())
            
            client.futures_change_leverage(symbol=symbol,leverage=leverage,timestamp=client.futures_time())

            bin_ret=client.futures_account_balance(timestamp=client.futures_time())
            
            for dic in bin_ret:
                if dic[ASSET] == USDT:
                    ret = dic
            
            balance=ret[WITHDRAW_AVAILABLE]

            quantity = round(((float(balance)*abs(engaged_balance)/entryPrice)-(5*10**(-precision - 1))), precision)

            if (quantity < (1*10**(-precision))):
                quantity = 1*10**(-precision)
            
            client.futures_create_order(symbol=symbol, side=SELL, positionSide=SHORT, type=MARKET, quantity=quantity ,timestamp=client.futures_time())

            ret = 0
        except:
            ret = 1
            err_cpt += 1
            print(FUNCTION)
            print(sys.exc_info())
            sleep(0.5)
    
    return ret