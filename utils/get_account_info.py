#!/usr/bin/python3
# -*- coding: utf-8 -*-

#######
# A "export PYTHONPATH=$PWD" needs to be done to run these functions
# Exemples of use:
# python3 get_account_info.py --keys AAAA BBBB --type S --symbol BTCUSDT
# python3 get_account_info.py -k AAAA BBBB -t S -s BTCUSDT
#######
#futures:
#2283846f8e2a3a1cc40e41900c21a38529a3261f8a32418710741f762a7637b1
#257e88264b63368063d3030893b0d9f9b1ae1032d703261ff787b2f4aae0cddd

#spot
#EYoXqgORlsC2q15AwiK30swZIBdrc1PVZZhMIoZlWEFUstIum0LdCPEm3eG7cF5y
#6hbXJ5kc9yRBl3VIHtKheQ0h6Fe5eG05cC99X3lBy5CzQvpBLUL4F1OkvyzhNRta
import argparse
import sys
from interface_binance import I__CLIENT, I__GET_ACCOUNT_HISTORY, I__SPOT_ACCOUNT_TRADES, I__FUTURES_ACCOUNT_TRADES
from constants import OUT, SPOT, FUTURES, BTCUSDT, ETHUSDT, PRICE
from strategy_file import *
# A "export PYTHONPATH=$PWD" needs to be done to run these functions

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keys", nargs='+', type=str, help="API keys")
    parser.add_argument("-t", "--type", type=str, choices=[SPOT, FUTURES, "S", "F"], help="account type")
    parser.add_argument("-s", "--symbol", type=str, choices=[BTCUSDT, ETHUSDT], help="Symbol")
    parser.add_argument("-m", "--mode", type=str, choices=['n', 'd'], default='d', help="Mode of execution")
    args = parser.parse_args()

    account_types_dict = {SPOT:SPOT, "S":SPOT, FUTURES:FUTURES, "F":FUTURES}
    """ Init of the master """
    """ ====================================================================== """
    master_api = ApiKeyMaster([str(args.keys[0]), str(args.keys[1]), OUT, \
                               account_types_dict[args.type], args.symbol])
    client = I__CLIENT(master_api.api_key, master_api.api_secret_key)
    client.API_URL = 'https://testnet.binance.vision/api'
    print(client.get_account())
    #print(client.enable_subaccount_futures())
    #print(client.get_margin_account())
    print(client.ping())
    
    #client.API_URL = 'https://testnet.binancefuture.com'
    """ ====================================================================== """
    
    trade_ret = I__GET_ACCOUNT_HISTORY(client, \
                              account_types_dict[args.type], master_api.symbol)
    print(trade_ret)
    
    #trade_ret = 0
    sys.exit(0)
    #sys.exit(trade_ret)
    
    