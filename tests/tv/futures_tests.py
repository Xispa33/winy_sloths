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
import multiprocessing
from functools import partial 

#python3 -m pytest --junitxml result.xml tests/tu/spot_tests.py -vxk "not test_compute_side"      
#SCRIPT_DIR=$PWD/scripts/ CEPS_DIR=$PWD/scripts/ceps/ SYMBOL=BTCUSDT ASSET=USDT python3 -m pytest tests/tu/binance/spot_tests.py -v
def run_winy_sloth(platform, return_dict, i):
    command_string = "python3 scripts/main.py --mode debug --folder " + os.getcwd() + "/tests/tv/TESTS/" + platform.lower() + "/" + FUTURES.lower() + "/" + \
                   " --history stats/"
    shell_command = subprocess.run(command_string, shell=True, capture_output=True)
    #print(command_string)
    ret = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
    return_dict[i] = ret

class SequentialTestLoader(unittest.TestLoader):
    def getTestCaseNames(self, testCaseClass):
        test_names = super().getTestCaseNames(testCaseClass)
        testcase_methods = list(testCaseClass.__dict__.keys())
        test_names.sort(key=testcase_methods.index)
        return test_names

class TestFuturesBinanceTV(unittest.TestCase):
    PLATFORM = os.getenv('PLATFORM')
    STRATEGY_FILE_NAME = os.getenv('STRAT_FILENAME')
    STRATEGY_FILE_PATH = os.getcwd() + "/tests/tv/TESTS/" + PLATFORM.lower() + "/futures/" + STRATEGY_FILE_NAME
    with open(STRATEGY_FILE_PATH, "r") as strategy_file:
        content = strategy_file.readlines()
        master_info = content[0].strip('\n').split(" ")
        PLATFORM_MASTER = master_info[0]
        API_KEY_MASTER = master_info[1]
        API_KEY_MASTER_SECRET = master_info[2]
        SYMBOL = master_info[5]
        slave_info = content[2].strip('\n').split(" ")
        PLATFORM_SLAVE = slave_info[0]
        API_KEY_SLAVE = slave_info[1]
        API_KEY_SLAVE_SECRET = slave_info[2]
        strategy_file.close()
        
    #info_strategy_file = [PLATFORM, API_KEY_MASTER, API_KEY_MASTER_SECRET, OUT, FUTURES, SYMBOL]
    info_strategy_file_master = [PLATFORM_MASTER, API_KEY_MASTER, API_KEY_MASTER_SECRET, OUT, FUTURES, SYMBOL]
    master_account = MasterAccount(info_strategy_file_master)
    obj_master = master_account.api_key.exchange_platform_obj
    
    info_strategy_file_slave = [PLATFORM_SLAVE, API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, FUTURES, SYMBOL]
    slave_account = SlaveAccount(info_strategy_file_slave, info_strategy_file_slave[4], info_strategy_file_slave[5])
    obj_slave = slave_account.api_key.exchange_platform_obj

    def test_nominal(self):
        jobs = []
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        #return_dict = {}

        p = multiprocessing.Process(target=run_winy_sloth, args=([self.info_strategy_file_master[0], return_dict, len(jobs)]))
        jobs.append(p)
        p.start()

        for proc in jobs:
            proc.join()
        
        # CHECK THAT WS RAN SUCCESSFULLY
        self.assertEqual(return_dict[0], 0)

        with open(self.STRATEGY_FILE_PATH, "r") as strategy_file:
            content = strategy_file.readlines()
            master_info = content[0].strip('\n').split(" ")
            slave_info = content[2].strip('\n').split(" ")
            master_position = master_info[3]
            slave_position = slave_info[3]
            strategy_file.close()
        
        self.assertEqual(master_position, OUT)
        self.assertEqual(slave_position, OUT)
       
    def test_open_close_long(self):
        # Tester position + strategy file
        return_dict = {}
        jobs = []
        manager = multiprocessing.Manager()
        return_dict_m = manager.dict()
        #return_dict = {}

        precision = self.obj_master.ALL_SYMBOLS_DICT[self.SYMBOL][PRECISION_IDX]
        asset = self.obj_master.ALL_SYMBOLS_DICT[self.SYMBOL][ASSET_IDX]
        leverage = 10
        engaged_balance = 4
        price = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__get_symbol_price_futures, \
                self.SYMBOL), retry=3, retry_period=2)
        
        
        bin_ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__get_futures_account_balance, \
                USDT), retry=3, retry_period=2)
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

        # ================== OPEN LONG ==================
        ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__open_long_futures, \
                self.SYMBOL, leverage, engaged_balance, \
                float(price[PRICE]), pct=1), retry=10, retry_period=2)
        self.assertEqual(ret, 0)

        time.sleep(1)

        ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__futures_account_trades, \
                self.SYMBOL))
        self.assertIsInstance(ret, list)

        ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__compute_side_futures_account, \
                self.master_account, ret))
        self.assertEqual(ret, LONG)

        p = multiprocessing.Process(target=run_winy_sloth, args=([self.info_strategy_file_master[0], return_dict_m, len(jobs)]))
        jobs.append(p)
        p.start()

        for proc in jobs:
            proc.join()
        
        # CHECK THAT WS RAN SUCCESSFULLY
        self.assertEqual(return_dict_m[0], 0)

        with open(self.STRATEGY_FILE_PATH, "r") as strategy_file:
            content = strategy_file.readlines()
            master_info = content[0].strip('\n').split(" ")
            slave_info = content[2].strip('\n').split(" ")
            master_position = master_info[3]
            slave_position = slave_info[3]
            strategy_file.close()
        
        self.assertEqual(master_position, LONG)
        self.assertEqual(slave_position, LONG)
        
        ret = self.obj_slave.CEP__BaseFunction(functools.partial( \
                self.obj_slave.cep__futures_account_trades, \
                self.SYMBOL))
        self.assertIsInstance(ret, list)

        ret = self.obj_slave.CEP__BaseFunction(functools.partial( \
                self.obj_slave.cep__compute_side_futures_account, \
                self.slave_account, ret))
        self.assertEqual(ret, LONG)
        # ================== OPEN LONG ==================

        # ================== CLOSE LONG ==================

        ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__close_long_futures, \
                self.SYMBOL), \
                retry=10, \
                retry_period=2)
        self.assertEqual(ret, 0)

        sleep(1)

        ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__futures_account_trades, \
                self.SYMBOL))
        self.assertIsInstance(ret, list)

        ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__compute_side_futures_account, \
                self.master_account, ret))
        self.assertEqual(ret, OUT)

        #run_winy_sloth(self.info_strategy_file_master[0], return_dict, 0)
        #self.assertEqual(return_dict[0], 0)
        
        jobs = []
        manager = multiprocessing.Manager()
        return_dict_m = manager.dict()

        p = multiprocessing.Process(target=run_winy_sloth, args=([self.info_strategy_file_master[0], return_dict_m, len(jobs)]))
        jobs.append(p)
        p.start()

        for proc in jobs:
            proc.join()
        
        # CHECK THAT WS RAN SUCCESSFULLY
        self.assertEqual(return_dict_m[0], 0)

        ret = self.obj_slave.CEP__BaseFunction(functools.partial( \
                self.obj_slave.cep__futures_account_trades, \
                self.SYMBOL))
        self.assertIsInstance(ret, list)

        ret = self.obj_slave.CEP__BaseFunction(functools.partial( \
                self.obj_slave.cep__compute_side_futures_account, \
                self.slave_account, ret))
        self.assertEqual(ret, OUT)
        
        # ================== CLOSE LONG ==================
        with open(self.STRATEGY_FILE_PATH, "r") as strategy_file:
            content = strategy_file.readlines()
            master_info = content[0].strip('\n').split(" ")
            slave_info = content[2].strip('\n').split(" ")
            master_position = master_info[3]
            slave_position = slave_info[3]
            strategy_file.close()
        
        self.assertEqual(master_position, OUT)
        self.assertEqual(slave_position, OUT)
    
    def test_open_close_short(self):
        # Tester position + strategy file
        return_dict = {}
        jobs = []
        manager = multiprocessing.Manager()
        return_dict_m = manager.dict()
        #return_dict = {}

        precision = self.obj_master.ALL_SYMBOLS_DICT[self.SYMBOL][PRECISION_IDX]
        asset = self.obj_master.ALL_SYMBOLS_DICT[self.SYMBOL][ASSET_IDX]
        leverage = 6
        engaged_balance = -3

        price = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__get_symbol_price_futures, \
                self.SYMBOL), retry=3, retry_period=2)

        # ================== OPEN SHORT ==================
        ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__open_short, \
                self.SYMBOL, leverage, engaged_balance, \
                float(price[PRICE]), 1), \
                retry=3, \
                retry_period=2)
        
        self.assertEqual(ret, 0)

        ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__futures_account_trades, \
                self.SYMBOL))
        self.assertIsInstance(ret, list)

        ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__compute_side_futures_account, \
                self.master_account, ret))
        self.assertEqual(ret, SHORT)

        p = multiprocessing.Process(target=run_winy_sloth, args=([self.info_strategy_file_master[0], return_dict_m, len(jobs)]))
        jobs.append(p)
        p.start()

        for proc in jobs:
            proc.join()
        
        # CHECK THAT WS RAN SUCCESSFULLY
        self.assertEqual(return_dict_m[0], 0)

        with open(self.STRATEGY_FILE_PATH, "r") as strategy_file:
            content = strategy_file.readlines()
            master_info = content[0].strip('\n').split(" ")
            slave_info = content[2].strip('\n').split(" ")
            master_position = master_info[3]
            slave_position = slave_info[3]
            strategy_file.close()
        
        self.assertEqual(master_position, SHORT)
        self.assertEqual(slave_position, SHORT)
        
        ret = self.obj_slave.CEP__BaseFunction(functools.partial( \
                self.obj_slave.cep__futures_account_trades, \
                self.SYMBOL))
        self.assertIsInstance(ret, list)

        ret = self.obj_slave.CEP__BaseFunction(functools.partial( \
                self.obj_slave.cep__compute_side_futures_account, \
                self.slave_account, ret))
        self.assertEqual(ret, SHORT)

        # ================== CLOSE SHORT ==================
        ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__close_short, \
                self.SYMBOL, pct=1), \
                retry=3, \
                retry_period=2)
        self.assertEqual(ret, 0)

        time.sleep(2)

        ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__futures_account_trades, \
                self.SYMBOL))
        self.assertIsInstance(ret, list)

        ret = self.obj_master.CEP__BaseFunction(functools.partial( \
                self.obj_master.cep__compute_side_futures_account, \
                self.master_account, ret))
        self.assertEqual(ret, OUT)

        jobs = []
        manager = multiprocessing.Manager()
        return_dict_m = manager.dict()

        p = multiprocessing.Process(target=run_winy_sloth, args=([self.info_strategy_file_master[0], return_dict_m, len(jobs)]))
        jobs.append(p)
        p.start()

        for proc in jobs:
            proc.join()
        
        # CHECK THAT WS RAN SUCCESSFULLY
        self.assertEqual(return_dict_m[0], 0)

        ret = self.obj_slave.CEP__BaseFunction(functools.partial( \
                self.obj_slave.cep__futures_account_trades, \
                self.SYMBOL))
        self.assertIsInstance(ret, list)

        ret = self.obj_slave.CEP__BaseFunction(functools.partial( \
                self.obj_slave.cep__compute_side_futures_account, \
                self.slave_account, ret))
        self.assertEqual(ret, OUT)

        with open(self.STRATEGY_FILE_PATH, "r") as strategy_file:
            content = strategy_file.readlines()
            master_info = content[0].strip('\n').split(" ")
            slave_info = content[2].strip('\n').split(" ")
            master_position = master_info[3]
            slave_position = slave_info[3]
            strategy_file.close()
        
        self.assertEqual(master_position, OUT)
        self.assertEqual(slave_position, OUT)

if __name__ == '__main__':
    unittest.main(testLoader=SequentialTestLoader())