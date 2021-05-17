import os
import subprocess
from time import *
from datetime import *
import unittest
from constants import LONG, SHORT, OUT, BTCUSDT, ETHUSDT, SPOT, FUTURES
from winy_sloth import WinySloth
from strategy_file import ApiKey, ApiKeyMaster
from password import API_KEY_SLAVE, API_KEY_SLAVE_SECRET, API_KEY_MASTER, API_KEY_MASTER_SECRET
import ast
import multiprocessing
from functools import partial

ACCOUNT_TYPE = SPOT
PATH = "tests/tv/TEST_" + ACCOUNT_TYPE + "/"

def test_compute_side(account, symbol, wait, return_dict, i):
        sleep(wait)
        shell_command = subprocess.run("python3 ./utils/get_account_info.py --keys " + account.api_key + " " + account.api_secret_key + " " + "--type S --symbol " + symbol, shell=True, capture_output=True)
        ret_get_info = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        pos = WinySloth.WinySloth__ComputeAccountSide(account, ret_get_info)
        return_dict[i] = pos

def run_winy_sloth_debug(symbol, return_dict, i):
    shell_command = subprocess.run("python3 main.py --mode debug --folder " + PATH + \
                   "/TEST_OUT_" + symbol + "/", shell=True, capture_output=True)
    ret = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
    return_dict[i] = ret

def open_long(master_api, account_type, symbol, wait, return_dict, i):
    sleep(wait)
    shell_command = subprocess.run("python3 ./utils/open_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t " + account_type + " -s " + symbol, shell=True, capture_output=True)
    ret_open_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
    return_dict[i] = ret_open_long

def close_long(master_api, account_type, symbol, wait, return_dict, i):
    sleep(wait)
    shell_command = subprocess.run("python3 ./utils/close_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t " + account_type + " -s " + symbol, shell=True, capture_output=True)
    ret_close_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
    return_dict[i] = ret_close_long

class TestSpot(unittest.TestCase):
    
    def test_eth_out(self):
        
        symbol = ETHUSDT
        jobs = []
        master_api = ApiKeyMaster([API_KEY_MASTER, API_KEY_MASTER_SECRET, OUT, ACCOUNT_TYPE, symbol])
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        p = multiprocessing.Process(target=run_winy_sloth_debug, args=([symbol, return_dict, len(jobs)]))
        jobs.append(p)
        p.start()

        p = multiprocessing.Process(target=test_compute_side, args=([master_api, symbol, 10, return_dict, len(jobs)]))
        jobs.append(p)
        p.start()

        for proc in jobs:
            proc.join()
        
        self.assertEqual(return_dict[0], 0)
        self.assertEqual(return_dict[1], OUT)
    
    def test_btc_out(self):
        
        symbol = BTCUSDT
        jobs = []
        master_api = ApiKeyMaster([API_KEY_MASTER, API_KEY_MASTER_SECRET, OUT, ACCOUNT_TYPE, symbol])
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        p = multiprocessing.Process(target=run_winy_sloth_debug, args=([symbol, return_dict, len(jobs)]))
        jobs.append(p)
        p.start()

        p = multiprocessing.Process(target=test_compute_side, args=([master_api, symbol, 10, return_dict, len(jobs)]))
        jobs.append(p)
        p.start()

        for proc in jobs:
            proc.join()
        
        self.assertEqual(return_dict[0], 0)
        self.assertEqual(return_dict[1], OUT)
    
    """
    # TEST BTC
    def test_long_btc(self):
        # INIT
        symbol = BTCUSDT
        jobs = []
        master_api = ApiKeyMaster([API_KEY_MASTER, API_KEY_MASTER_SECRET, OUT, ACCOUNT_TYPE, symbol])
        slave_api = ApiKey([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT)
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        p = multiprocessing.Process(target=run_winy_sloth_debug, args=([symbol, return_dict, len(jobs)]))
        jobs.append(p)
        p.start()

        p = multiprocessing.Process(target=open_long, args=([master_api, ACCOUNT_TYPE, symbol, 1, return_dict, len(jobs)]))
        jobs.append(p)
        p.start()

        p = multiprocessing.Process(target=close_long, args=([master_api, ACCOUNT_TYPE, symbol, 10, return_dict, len(jobs)]))
        jobs.append(p)
        p.start()

        times_s = [5, 15]
        for time in times_s:
            p = multiprocessing.Process(target=test_compute_side, args=([master_api, symbol, time, return_dict, len(jobs)]))
            jobs.append(p)
            p.start()

            p = multiprocessing.Process(target=test_compute_side, args=([slave_api, symbol, time, return_dict, len(jobs)]))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()
        
        self.assertEqual(return_dict[0], 0)
        self.assertEqual(return_dict[1], 0)
        self.assertEqual(return_dict[2], 0)
        self.assertEqual(return_dict[1], LONG)
        self.assertEqual(return_dict[2], LONG)
        self.assertEqual(return_dict[1], OUT)
        self.assertEqual(return_dict[2], OUT)

    
    # TEST ETH
    def test_long_eth(self):
        # INIT
        symbol = ETHUSDT
        jobs = []
        master_api = ApiKeyMaster([API_KEY_MASTER, API_KEY_MASTER_SECRET, OUT, ACCOUNT_TYPE, symbol])
        slave_api = ApiKey([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT)
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        p = multiprocessing.Process(target=run_winy_sloth_debug, args=([symbol, return_dict, len(jobs)]))
        jobs.append(p)
        p.start()

        p = multiprocessing.Process(target=open_long, args=([master_api, ACCOUNT_TYPE, symbol, 1, return_dict, len(jobs)]))
        jobs.append(p)
        p.start()

        p = multiprocessing.Process(target=close_long, args=([master_api, ACCOUNT_TYPE, symbol, 10, return_dict, len(jobs)]))
        jobs.append(p)
        p.start()

        times_s = [5, 15]
        for time in times_s:
            p = multiprocessing.Process(target=test_compute_side, args=([master_api, symbol, time, return_dict, len(jobs)]))
            jobs.append(p)
            p.start()

            p = multiprocessing.Process(target=test_compute_side, args=([slave_api, symbol, time, return_dict, len(jobs)]))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()
        
        self.assertEqual(return_dict[0], 0)
        self.assertEqual(return_dict[1], 0)
        self.assertEqual(return_dict[2], 0)
        self.assertEqual(return_dict[1], LONG)
        self.assertEqual(return_dict[2], LONG)
        self.assertEqual(return_dict[1], OUT)
        self.assertEqual(return_dict[2], OUT)
    """
if __name__ == '__main__':
    unittest.main()

#coverage run -m --source=. pytest --junitxml toto.xml tests/tv/spot_tests.py -vxk "not test_compute_side"
#coverage report or coverage html
#coverage run -m pytest tests/tv/spot_tests.py -vxk  "not test_compute_side"; coverage combine; coverage report