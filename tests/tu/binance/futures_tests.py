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
    open_close_flag = True

    def test_get_futures_time(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__futures_time), retry=3, retry_period=2)
        self.assertIsInstance(ret, int)
        self.assertGreater(ret, int(time.time()*1000) - 3600)
        sleep(1)
    
    def test_futures_open_orders(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__get_futures_open_orders, self.symbol), \
                retry=3, retry_period=2)
        self.assertIsInstance(ret, list)
        self.assertEqual(len(ret), 0)
        self.open_close_flag = len(ret)==0 & self.open_close_flag
    
    def test_get_futures_account_balance(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__get_futures_account_balance, \
                self.asset), retry=3, retry_period=2)
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret[ASSET], self.asset)
        sleep(1)
    
    def test_get_futures_account_trades(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__futures_account_trades, \
                self.symbol), retry=3, retry_period=2)
        self.assertIsInstance(ret, list)
        sleep(1)
    
    def test_get_symbol_price_futures(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__get_symbol_price_futures, \
                self.symbol), retry=3, retry_period=2)
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret[SYMBOL], self.symbol)
        self.assertIsInstance(ret[SYMBOL], str)
        self.assertGreater(float(ret[PRICE]), 0)
        sleep(1)

    def test_compute_side_futures_account(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__futures_account_trades, \
                self.symbol), retry=3, retry_period=2)
        pos = self.obj_binance.cep__compute_side_futures_account(self.account,ret)
        self.assertEqual(pos, OUT)
        sleep(1)
    
    def test_futures_position_mode(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__futures_position_mode), \
                retry=3, retry_period=2)
        self.assertIsInstance(ret,dict)
        self.assertEqual(ret['dualSidePosition'],True)
    
    def test_futures_change_position_mode(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__futures_change_position_mode), \
                retry=3, retry_period=2)
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret['msg'], 'success')

        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__futures_change_position_mode, \
                TRUE), retry=3, retry_period=2)
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret['msg'], 'success')
    
    def test_futures_change_leverage(self):
        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__futures_change_leverage, \
                self.symbol, 5), retry=3, retry_period=2)
        self.assertIsInstance(ret,dict)
        self.assertEqual(ret[LEVERAGE], 5)

        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__futures_change_leverage, \
                self.symbol, BINANCE_DEFAULT_LEVERAGE), retry=3, retry_period=2)
        self.assertIsInstance(ret,dict)
        self.assertEqual(ret[LEVERAGE], BINANCE_DEFAULT_LEVERAGE)

    @unittest.skipIf(open_close_flag==False, "This test was skipped because the account position side is not out.")
    def test_open_close_long_futures(self):
        precision = self.obj_binance.ALL_SYMBOLS_DICT[self.symbol][PRECISION_IDX]
        asset = self.obj_binance.ALL_SYMBOLS_DICT[self.symbol][ASSET_IDX]
        leverage = 10
        engaged_balance = 4
        price = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__get_symbol_price_futures, \
                self.symbol), retry=3, retry_period=2)
        
        
        bin_ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__get_futures_account_balance, \
                self.asset), retry=3, retry_period=2)
        if (isinstance(bin_ret, list)):
            for dic in bin_ret:
                if dic[ASSET] == USDT:
                    ret = dic
        elif (isinstance(bin_ret, dict)):
            ret = bin_ret
        else:
            raise ValueError("bin_ret variable is bad.\nType is:{}\nValue is:{}\n".format( \
                type(bin_ret), bin_ret))
        balance = ret[MAX_WITHDRAW_AMOUNT]
        quantity=round(((float(balance)*engaged_balance/float(price[PRICE])) - \
                                        (5*10**(-precision-1))),precision)
        delta = (2*10**(-precision+1))
        sleep(1)

        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__open_long_futures, \
                self.symbol, leverage, engaged_balance, \
                float(price[PRICE]), pct=1), retry=10, retry_period=2)
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret[SIDE], 'BUY')
        self.assertEqual(ret['positionSide'], LONG)
        new_qty = float(ret['executedQty'])
        self.assertAlmostEqual(quantity, new_qty, None, "Not equal", delta)

        sleep(1)

        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__close_long_futures, \
                self.symbol), \
                retry=10, \
                retry_period=2)
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret['status'], 'FILLED')
        self.assertEqual(ret[SIDE], 'SELL')
        self.assertEqual(ret['positionSide'], LONG)
        new_qty = float(ret['executedQty'])
        self.assertAlmostEqual(quantity, new_qty, None, "Not equal", delta)
    
    @unittest.skipIf(open_close_flag==False, "This test was skipped because the account position side is not out.")
    def test_open_close_short_futures(self):
        leverage = 6
        engaged_balance = -3
        price = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__get_symbol_price_futures, \
                self.symbol), \
                retry=MAX_RETRY, \
                retry_period=2)
        
        time.sleep(1)

        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__open_short, \
                self.symbol, leverage, engaged_balance, \
                float(price[PRICE]), 1), \
                retry=3, \
                retry_period=2)
        self.assertIsInstance(ret, dict)

        time.sleep(1)

        ret = self.obj_binance.CEP__BaseFunction(functools.partial( \
                self.obj_binance.cep__close_short, \
                self.symbol), \
                retry=3, \
                retry_period=2)
        self.assertIsInstance(ret, dict)

if __name__ == '__main__':
    unittest.main(testLoader=SequentialTestLoader())
