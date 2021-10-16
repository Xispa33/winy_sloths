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
class SequentialTestLoader(unittest.TestLoader):
    def getTestCaseNames(self, testCaseClass):
        test_names = super().getTestCaseNames(testCaseClass)
        testcase_methods = list(testCaseClass.__dict__.keys())
        test_names.sort(key=testcase_methods.index)
        return test_names
        
class TestFuturesBybit(unittest.TestCase):
    symbol = os.getenv('SYMBOL')
    asset = os.getenv('ASSET')
    info_strategy_file = [BYBIT, API_KEY_MASTER_FUTURES_2, API_KEY_MASTER_SECRET_FUTURES_2, OUT, FUTURES, symbol]
    
    account = MasterAccount(info_strategy_file)
    obj_bybit = account.api_key.exchange_platform_obj
    obj_bybit.cep__client(account.api_key.client._api_key, account.api_key.client._api_secret_key, account.account_contract_type)
    open_close_flag = True

    def test_get_futures_time(self):
        ret = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                self.obj_bybit.cep__futures_time), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertIsInstance(ret, int)
        real_time = str(int(time.time()*1000))[:-3]
        self.assertGreater(ret, int(real_time) - 3600)
        sleep(1)

    def test_get_futures_account_balance(self):
        ret = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                self.obj_bybit.cep__get_futures_account_balance, \
                self.asset), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertIsInstance(ret, dict)
        #self.assertEqual(ret[ASSET], self.asset)
        sleep(1)
    
    def test_get_futures_account_trades(self):
        ret = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                self.obj_bybit.cep__futures_account_trades, \
                self.symbol), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertIsInstance(ret, list)
        sleep(1)
    
    def test_get_symbol_price_futures(self):
        ret = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                self.obj_bybit.cep__get_symbol_price_futures, \
                self.symbol), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertIsInstance(ret, list)
        sleep(1)

    def test_compute_side_futures_account(self):
        ret = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                self.obj_bybit.cep__futures_account_trades, \
                self.symbol), \
                retry=MAX_RETRY, \
                retry_period=2)
        self.assertIsInstance(ret, list)

        pos = self.obj_bybit.cep__compute_side_futures_account(self.account, ret)
        self.assertEqual(pos, OUT)
        sleep(1)
    
    def test_get_my_futures_position(self):
        ret = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                self.obj_bybit.cep__get_my_futures_positions, \
                self.symbol), \
                retry=3, \
                retry_period=2)
        self.assertIsInstance(ret, list)
    
    def test_change_futures_leverage(self):
        leverages = [BYBIT_MAX_LEVERAGE, BYBIT_DEFAULT_LEVERAGE]
        for leverage in leverages:
            ret = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                    self.obj_bybit.cep__futures_change_leverage, \
                    self.symbol, leverage), \
                    retry=MAX_RETRY, \
                    retry_period=2)
            self.assertIsInstance(ret, dict)
            self.assertEqual(ret['ret_msg'], 'OK')
            sleep(1)
        
    @unittest.skipIf(open_close_flag==False, "This test was skipped because the account position side is not out.")
    def test_open_close_long_futures(self):
        leverage = 20
        engaged_balance = 7
        price = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                self.obj_bybit.cep__get_symbol_price_futures, \
                self.symbol), \
                retry=MAX_RETRY, \
                retry_period=2)
        
        time.sleep(1)

        ret = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                self.obj_bybit.cep__open_long_futures, \
                self.symbol, leverage, engaged_balance, \
                float(price[0]['last_price']), 1), \
                retry=3, \
                retry_period=2)
        self.assertIsInstance(ret, dict)

        time.sleep(1)

        ret = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                self.obj_bybit.cep__close_long_futures, \
                self.symbol), \
                retry=3, \
                retry_period=2)
        self.assertIsInstance(ret, dict)
        
    @unittest.skipIf(open_close_flag==False, "This test was skipped because the account position side is not out.")
    def test_open_close_short_futures(self):
        leverage = 6
        engaged_balance = -3
        price = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                self.obj_bybit.cep__get_symbol_price_futures, \
                self.symbol), \
                retry=MAX_RETRY, \
                retry_period=2)
        
        time.sleep(1)

        ret = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                self.obj_bybit.cep__open_short, \
                self.symbol, leverage, engaged_balance, \
                float(price[0]['last_price']), 1), \
                retry=3, \
                retry_period=2)
        self.assertIsInstance(ret, dict)

        time.sleep(1)

        ret = self.obj_bybit.CEP__BaseFunction(functools.partial( \
                self.obj_bybit.cep__close_short, \
                self.symbol), \
                retry=3, \
                retry_period=2)
        self.assertIsInstance(ret, dict)

if __name__ == '__main__':
    unittest.main(testLoader=SequentialTestLoader())
