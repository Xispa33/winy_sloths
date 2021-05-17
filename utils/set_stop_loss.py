#!/usr/bin/python3
# -*- coding: utf-8 -*-

#######
# A "export PYTHONPATH=$PWD" needs to be done to run these functions
#
# Examples of use:
# python3 set_stop_loss.py --keys AAAA BBBB -s BTCUSDT --engaged_balance 1 --risk 0
# python3 set_stop_loss.py --keys AAAA BBBB -s ETHUSDT -r 0 -p 2450.0 -m H
# python3 set_stop_loss.py --keys AAAA BBBB -s ETHUSDT -r 0 -p 2450.0 --mode ONE_WAY
#######

import argparse
import sys
from interface_binance import I__CLIENT, \
    I__MANAGE_STOP_LOSS
from constants import OUT, SPOT, FUTURES, PRICE, \
                      BTCUSDT, ETHUSDT, LONG, SHORT, RISK, \
                      HEDGE, ONE_WAY
from strategy_file import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keys", nargs='+', type=str, help="API keys")
    parser.add_argument("-s", "--symbol", type=str, choices=[BTCUSDT, ETHUSDT], help="Symbol")
    parser.add_argument("-t", "--type", type=str, choices=[SHORT, LONG], help="Symbol")
    parser.add_argument("-e", "--engaged_balance", type=float, help="Engaged balance", default = 1.0)
    parser.add_argument("-r", "--risk", type=float, help="Risk", default = RISK)
    parser.add_argument("-p", "--price", type=float, help="Price")
    parser.add_argument("-m", "--mode", type=str, help="Mode")
    args = parser.parse_args()

    mode_dict = {HEDGE:HEDGE, "H":HEDGE, ONE_WAY:ONE_WAY, "O":ONE_WAY}
    
    """ Init of the master """
    """ ====================================================================== """
    master_api = ApiKeyMaster([str(args.keys[0]), str(args.keys[1]), OUT, \
                               FUTURES, args.symbol])
    client = I__CLIENT(master_api.api_key, master_api.api_secret_key)
    master_api.engaged_balance = args.engaged_balance
    #master_api.entryPrice = float(client.get_avg_price(symbol=master_api.symbol)[PRICE])
    master_api.entryPrice = args.price
    master_api.side = args.type
    risk = args.risk
    """ ====================================================================== """
    if (master_api.side == LONG or master_api.side == SHORT):
        ret_set_sl = I__MANAGE_STOP_LOSS(client, master_api.symbol, \
                                         master_api.engaged_balance, \
                                         master_api.entryPrice, \
                                         master_api.side, \
                                         mode = mode_dict[args.mode], \
                                         risk = risk)
    else: 
        ret_set_sl = 1
    
    print(ret_set_sl)
    #trade_ret = 0
    sys.exit(ret_set_sl)
    
    