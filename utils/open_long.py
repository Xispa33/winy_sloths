#!/usr/bin/python3
# -*- coding: utf-8 -*-

#######
# A "export PYTHONPATH=$PWD" needs to be done to run these functions
#
# Examples of use:
# python3 open_long.py --keys AAAA BBBB --type S --symbol ETHUSDT
# python3 open_long.py -k AAAA BBBB -t SPOT -s BTCUSDT
# python3 open_long.py --keys AAAA BBBB --type SPOT -s BTCUSDT --leverage 3 --engaged_balance 0.5
#######

import argparse
import sys
from interface_binance import I__CLIENT, \
     I__OPEN_LONG, I__OPEN_LONG_FUTURES, I__OPEN_LONG_SPOT, \
     I__GET_ACCOUNT_HISTORY
from constants import OUT, SPOT, FUTURES, PRICE, BTCUSDT, ETHUSDT
from strategy_file import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keys", nargs='+', type=str, help="API keys")
    parser.add_argument("-t", "--type", type=str, choices=[SPOT, FUTURES, "S", "F"], help="Account type")
    parser.add_argument("-s", "--symbol", type=str, choices=[BTCUSDT, ETHUSDT], help="Symbol")
    parser.add_argument("-l", "--leverage", type=str, help="Leverage", default='1')
    parser.add_argument("-e", "--engaged_balance", type=float, help="Engaged balance", default = 1.0)
    parser.add_argument("-m", "--mode", type=str, choices=['n', 'd'], default='d', help="Mode of execution")
    args = parser.parse_args()

    account_types_dict = {SPOT:SPOT, "S":SPOT, FUTURES:FUTURES, "F":FUTURES}
    
    """ Init of the master """
    """ ====================================================================== """
    master_api = ApiKeyMaster([str(args.keys[0]), str(args.keys[1]), OUT, \
                               account_types_dict[args.type], args.symbol])
    client = I__CLIENT(master_api.api_key, master_api.api_secret_key)
    master_api.leverage = str(args.leverage)
    master_api.engaged_balance = args.engaged_balance
    master_api.entryPrice = float(client.get_avg_price(symbol=master_api.symbol)[PRICE])
    """ ====================================================================== """
    client = I__CLIENT(master_api.api_key, master_api.api_secret_key)
    
    if (str(args.mode) == 'd'):
        client.API_URL = 'https://testnet.binance.vision/api'
    
    trade_ret = I__OPEN_LONG(client, master_api)
    #trade_ret = 0
    sys.exit(trade_ret)
    
    