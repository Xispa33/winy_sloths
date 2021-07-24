#!/usr/bin/python3
# -*- coding: utf-8 -*-

#######
# A "export PYTHONPATH=$PWD" needs to be done to run these functions
# Exemples of use:
# python3 close_long.py --keys AAAA BBBB --type S --symbol BTCUSDT
# python3 close_long.py -k AAAA BBBB -t FUTURES -s ETHUSDT
#######

import argparse
import sys
from interface_binance import I__CLIENT, I__CLOSE_LONG, I__CLOSE_LONG_FUTURES, I__CLOSE_LONG_SPOT
from constants import OUT, SPOT, FUTURES, BTCUSDT, ETHUSDT, BNBUSDT
from strategy_file import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keys", nargs='+', type=str, help="API keys")
    parser.add_argument("-t", "--type", type=str, choices=[SPOT, FUTURES, "S", "F"], help="Account type")
    parser.add_argument("-s", "--symbol", type=str, choices=[BTCUSDT, ETHUSDT, BNBUSDT], help="Symbol")
    args = parser.parse_args()

    account_types_dict = {SPOT:SPOT, "S":SPOT, FUTURES:FUTURES, "F":FUTURES}
    """ Init of the master """
    """ ====================================================================== """
    master_api = ApiKeyMaster([str(args.keys[0]), str(args.keys[1]), OUT, \
                               account_types_dict[args.type], args.symbol])
    """ ====================================================================== """
    client = I__CLIENT(master_api.api_key, master_api.api_secret_key)
    
    trade_ret = I__CLOSE_LONG(client, master_api)
    print(trade_ret)
    #trade_ret = 0
    sys.exit(trade_ret)
    
    