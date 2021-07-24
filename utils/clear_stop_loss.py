#!/usr/bin/python3
# -*- coding: utf-8 -*-

#######
# A "export PYTHONPATH=$PWD" needs to be done to run these functions
#
# Examples of use:
# python3 clear_stop_loss.py --keys AAAA BBBB -s BTCUSDT
# python3 clear_stop_loss.py --keys AAAA BBBB -s ETHUSDT
#######

import argparse
import sys
from interface_binance import I__CLIENT, \
    I__CLEAR_STOP_LOSS
from constants import FUTURES, OUT, BTCUSDT, ETHUSDT, BNBUSDT
from strategy_file import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keys", nargs='+', type=str, help="API keys")
    parser.add_argument("-s", "--symbol", type=str, choices=[BTCUSDT, ETHUSDT, BNBUSDT], help="Symbol")
    args = parser.parse_args()

    """ Init of the master """
    """ ====================================================================== """
    master_api = ApiKeyMaster([str(args.keys[0]), str(args.keys[1]), OUT, \
                               FUTURES, args.symbol])
    """ ====================================================================== """
    client = I__CLIENT(master_api.api_key, master_api.api_secret_key)
    
    ret_stop_sl = I__CLEAR_STOP_LOSS(client, master_api.symbol)
    
    print(ret_stop_sl)
    #trade_ret = 0
    sys.exit(ret_stop_sl)
    
    