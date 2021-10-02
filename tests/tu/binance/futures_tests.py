#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess
from time import *
from datetime import *
import unittest
import ast
sys.path.append(os.getenv('SCRIPT_DIR'))
from constants import *
sys.path.append(os.getenv('CEPS_DIR') + "binance")
sys.path.append(os.getenv('CEPS_DIR') + "bybit") 
from strategy_file import *
from password import *

#python3 -m pytest --junitxml result.xml tests/tu/spot_tests.py -vxk "not test_compute_side"      
#SCRIPT_DIR=$PWD/scripts/ CEPS_DIR=$PWD/scripts/ceps/ SYMBOL=BTCUSDT ASSET=USDT python3 -m pytest tests/tu/binance/futures_tests.py -v

class TestFuturesBinance(unittest.TestCase):
    symbol = os.getenv('SYMBOL')
    asset = os.getenv('ASSET')
    info_strategy_file = [BINANCE, API_KEY_MASTER_FUTURES_1, API_KEY_MASTER_SECRET_FUTURES_1, OUT, FUTURES, symbol]
    
    account = MasterAccount(info_strategy_file)
    obj_binance = account.api_key.exchange_platform_obj
    obj_binance.cep__client(account.api_key.client._api_key, account.api_key.client._api_secret_key, account.account_contract_type)

    def test_get_futures_time(self):
        ret = self.obj_binance.cep__futures_time()
        self.assertIsInstance(ret, int)
        self.assertGreater(ret, int(time.time()*1000) - 3600)
    
    def test_get_futures_account_balance(self):
        ret = self.obj_binance.cep__get_futures_account_balance(self.asset)
        print(ret)
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret[ASSET], self.asset)
    
    def test_get_futures_account_trades(self):
        ret = self.obj_binance.cep__futures_account_trades(self.symbol)
        self.assertIsInstance(ret, list)
    
    def test_get_symbol_price_futures(self):
        ret = self.obj_binance.cep__get_symbol_price_futures(self.symbol)
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret[SYMBOL], self.symbol)
        self.assertIsInstance(ret[SYMBOL], str)
        self.assertGreater(float(ret[PRICE]), 0)

    """
    def test_open_long_futures(self, symbol):
        price = ?
        ret = obj_binance.CEP__BaseFunction(functools.partial( \
                            obj_binance.cep__open_long_futures, \
                            symbol, 1, 1, price), \
                            retry=MAX_RETRY*10, \
                            retry_period=0.5)

        self.assertEqual(ret, 0)

        ret = obj_binance.CEP__BaseFunction(functools.partial( \
                            obj_binance.cep__futures_account_trades, \
                            symbol))
        self.assertIsInstance(ret, list)
        
        account = 
        ret = obj_binance.CEP__BaseFunction(functools.partial( \
                            obj_binance.cep__compute_side_futures_account, \
                            account, ret))
        self.assertEqual(ret, LONG)

    def test_close_long_futures(self, symbol):
        price = ?
        ret = obj_binance.CEP__BaseFunction(functools.partial( \
                            obj_binance.cep__close_long_futures, \
                            symbol, 1, 1, price), \
                            retry=MAX_RETRY*10, \
                            retry_period=0.5)
        self.assertEqual(ret, 0)

        ret = obj_binance.CEP__BaseFunction(functools.partial( \
                            obj_binance.cep__futures_account_trades, \
                            symbol))
        self.assertIsInstance(ret, list)
        
        account = 
        ret = obj_binance.CEP__BaseFunction(functools.partial( \
                            obj_binance.cep__compute_side_futures_account, \
                            account, ret))
        self.assertEqual(ret, OUT)

    def test_open_short_futures(self, symbol):
        price = ?
        ret = obj_binance.CEP__BaseFunction(functools.partial( \
                            obj_binance.cep__open_short, \
                            symbol, 1, 1, price), \
                            retry=MAX_RETRY*10, \
                            retry_period=0.5)

        self.assertEqual(ret, 0)
        
        ret = obj_binance.CEP__BaseFunction(functools.partial( \
                            obj_binance.cep__futures_account_trades, \
                            symbol))
        self.assertIsInstance(ret, list)
        
        account = 
        ret = obj_binance.CEP__BaseFunction(functools.partial( \
                            obj_binance.cep__compute_side_futures_account, \
                            account, ret))
        self.assertEqual(ret, SHORT)

    def test_close_short_futures(self, symbol):
        price = ?
        ret = obj_binance.CEP__BaseFunction(functools.partial( \
                            obj_binance.cep__close_short, \
                            symbol, 1, 1, price), \
                            retry=MAX_RETRY*10, \
                            retry_period=0.5)
        self.assertEqual(ret, 0)

        ret = obj_binance.CEP__BaseFunction(functools.partial( \
                            obj_binance.cep__futures_account_trades, \
                            symbol))
        self.assertIsInstance(ret, list)
        
        account = 
        ret = obj_binance.CEP__BaseFunction(functools.partial( \
                            obj_binance.cep__compute_side_futures_account, \
                            account, ret))
        self.assertEqual(ret, OUT)
    """
if __name__ == '__main__':
    unittest.main()