#!/usr/bin/python3
# -*- coding: utf-8 -*-

#######
# A "export PYTHONPATH=$PWD" needs to be done to run these functions
# Exemples of use:
# python3 open_long.py --keys AAAA BBBB --type S --symbol BTCUSDT
# python3 open_long.py -k AAAA BBBB -t S -s BTCUSDT
#######

import argparse
import sys
from interface_binance import I__CLIENT, I__OPEN_SHORT
from constants import OUT, SPOT, FUTURES, BTCUSDT, ETHUSDT, PRICE
from strategy_file import *
# A "export PYTHONPATH=$PWD" needs to be done to run these functions

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keys", nargs='+', type=str, help="API keys")
    parser.add_argument("-t", "--type", type=str, choices=[SPOT, FUTURES, "S", "F"], help="account type")
    parser.add_argument("-s", "--symbol", type=str, choices=[BTCUSDT, ETHUSDT], help="Symbol")
    parser.add_argument("-l", "--leverage", type=str, help="Leverage", default='1')
    parser.add_argument("-e", "--engaged_balance", type=int, help="Engaged balance", default = 1)
    args = parser.parse_args()

    account_types_dict = {SPOT:SPOT, "S":SPOT, FUTURES:FUTURES, "F":FUTURES}
    """ Init of the master """
    """ ====================================================================== """
    master_api = ApiKeyMaster([str(args.keys[0]), str(args.keys[1]), OUT, \
                               account_types_dict[args.type], args.symbol])
    client = I__CLIENT(master_api.api_key, master_api.api_secret_key)
    master_api.leverage = str(args.leverage)
    master_api.engaged_balance = args.engaged_balance
    master_api.entryPrice = client.get_avg_price(symbol=master_api.symbol)[PRICE]
    """ ====================================================================== """

    trade_ret = I__OPEN_SHORT(I__CLIENT(master_api.api_key, master_api.api_secret_key), \
                              master_api.symbol, master_api.leverage, \
                              master_api.engaged_balance, master_api.entryPrice)
    #trade_ret = 0
    sys.exit(trade_ret)
    
    