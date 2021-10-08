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
import pytest


#python3 -m pytest --junitxml result.xml tests/tu/spot_tests.py -vxk "not test_compute_side"      
#SCRIPT_DIR=$PWD/scripts/ CEPS_DIR=$PWD/scripts/ceps/ SYMBOL=BTCUSDT ASSET=USDT python3 -m pytest tests/tu/binance/spot_tests.py -v

class TestSpot(unittest.TestCase):
    symbol = os.getenv('SYMBOL')
    asset = os.getenv('ASSET')
    info_strategy_file = [BINANCE, API_KEY_MASTER_SPOT_1, API_KEY_MASTER_SECRET_SPOT_1, OUT, SPOT, symbol]
    
    account = MasterAccount(info_strategy_file)
    obj_binance = account.api_key.exchange_platform_obj
    obj_binance.cep__client(account.api_key.client._api_key, account.api_key.client._api_secret_key, account.account_contract_type)
    open_close_flag = True

    def test_get_avg_price(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.get_avg_price, \
                self.symbol), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertIsInstance(ret, dict)
        self.assertGreater(round(float(ret[PRICE]),2), 0)
        sleep(1)
    
    def test_get_asset_balance(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.get_asset_balance, \
                self.asset), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertIsInstance(ret, dict)
        self.assertGreater(round(float(ret[FREE]),2), 0)
        sleep(1)
    
    def test_get_symbol_price_ticker(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__get_symbol_price_ticker, \
                self.symbol), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret[SYMBOL], self.symbol)
        self.assertGreater(round(float(ret[PRICE]),2), 0)
        sleep(1)
    
    def test_get_order_book(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__get_order_book, \
                self.symbol), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertIsInstance(ret, dict)
        sleep(1)

    def test_get_aggregate_trades(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__get_aggregate_trades, \
                self.symbol), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertIsInstance(ret, list)
        sleep(1)

    def test_get_exchange_info(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__get_exchange_info), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertIsInstance(ret['symbols'], list)
        sleep(1)

    def test_spot_account_trades(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__spot_account_trades, \
                self.symbol), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertIsInstance(ret, list)
        sleep(1)
    
    def test_compute_side(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__spot_account_trades, \
                self.symbol))
        self.assertIsInstance(ret, list)
        
        self.open_close_flag = isinstance(ret, list)

        ret = self.obj_binance.cep__compute_side_spot_account(self.account, ret)
        self.assertEqual(ret, OUT)
        self.open_close_flag = isinstance(ret, list) & self.open_close_flag
        sleep(1)

    @unittest.skipIf(open_close_flag==False, "This test was skipped because the account position side is not out.")
    def test_open_close_order(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__open_long_spot, \
                self.symbol, False, 1), \
                retry=10, \
                retry_period=0.5)
        self.assertEqual(ret, 0)
                
        sleep(2)

        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__spot_account_trades, \
                self.symbol))
        self.assertIsInstance(ret, list)
        
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__compute_side_spot_account, \
                self.account, ret))
        self.assertEqual(ret, LONG)

        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__close_long_spot, \
                self.symbol, False, 1), \
                retry=10, \
                retry_period=0.5)
        self.assertEqual(ret, 0)
                
        sleep(2)

        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__spot_account_trades, \
                self.symbol))
        self.assertIsInstance(ret, list)
        
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__compute_side_spot_account, \
                self.account, ret))
        self.assertEqual(ret, OUT)

        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.get_asset_balance, \
                USDT), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertGreater(round(float(ret[FREE]),2), 50)
        
if __name__ == '__main__':
    unittest.main()
