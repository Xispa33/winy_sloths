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
"""
try:
    from pytest_cov.embed import cleanup_on_sigterm
except ImportError:
    pass
else:
    cleanup_on_sigterm()
"""
#python3 -m pytest --junitxml result.xml tests/tu/spot_tests.py -vxk "not test_compute_side"      

PATH = "tests/tv/TEST_SPOT/"
ACCOUNT_TYPE = SPOT

def test_compute_side(account, symbol, wait, return_dict):
        sleep(wait)
        shell_command = subprocess.run("python3 ./utils/get_account_info.py --keys " + account.api_key + " " + account.api_secret_key + " " + "--type S --symbol " + symbol, shell=True, capture_output=True)
        ret_get_info = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        pos = WinySloth.WinySloth__ComputeAccountSide(account, ret_get_info)
        return_dict[0] = pos

def run_winy_sloth_debug(symbol, return_dict):
    shell_command = subprocess.run("python3 main.py --mode debug --folder " + PATH + \
                   "/TEST_OUT_" + symbol + "/", shell=True, capture_output=True)
    ret = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
    return_dict[1] = ret

def open_long(master_api, account_type, symbol, wait):
    sleep(wait)
    shell_command = subprocess.run("python3 ./utils/open_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t " + account_type + " -s " + symbol, shell=True, capture_output=True)
    ret_open_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
    return ret_open_long


def close_long(master_api, account_type, symbol, wait):
    sleep(wait)
    shell_command = subprocess.run("python3 ./utils/close_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t " + account_type + " -s " + symbol, shell=True, capture_output=True)
    ret_close_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
    return ret_close_long

class TestSpot(unittest.TestCase):
    
    def test_eth_out(self):
        
        symbol = ETHUSDT
        jobs = []
        master_api = ApiKeyMaster([API_KEY_MASTER, API_KEY_MASTER_SECRET, OUT, ACCOUNT_TYPE, symbol])
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        p = multiprocessing.Process(target=run_winy_sloth_debug, args=([symbol, return_dict]))
        jobs.append(p)
        p.start()

        p = multiprocessing.Process(target=test_compute_side, args=([master_api, symbol, 10, return_dict]))
        jobs.append(p)
        p.start()

        for proc in jobs:
            proc.join()
        
        self.assertEqual(return_dict[0], OUT)
        self.assertEqual(return_dict[1], 0)
    
    def test_btc_out(self):
        
        symbol = BTCUSDT
        jobs = []
        master_api = ApiKeyMaster([API_KEY_MASTER, API_KEY_MASTER_SECRET, OUT, ACCOUNT_TYPE, symbol])
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        p = multiprocessing.Process(target=run_winy_sloth_debug, args=([symbol, return_dict]))
        jobs.append(p)
        p.start()

        p = multiprocessing.Process(target=test_compute_side, args=([master_api, symbol, 10, return_dict]))
        jobs.append(p)
        p.start()

        for proc in jobs:
            proc.join()
        
        self.assertEqual(return_dict[0], OUT)
        self.assertEqual(return_dict[1], 0)
    
    """
    # TEST BTC
    def test_long_btc(self):
        # INIT
        symbol = BTCUSDT
        master_api = ApiKeyMaster([API_KEY_MASTER, API_KEY_MASTER_SECRET, OUT, ACCOUNT_TYPE, symbol])
        slave_api = ApiKey([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT)
        ray.init()

        # OPEN LONG + CLOSE LONG
        ret1, ret2, ret3, ret4, ret5, ret6, ret7 = ray.get([ \
            run_winy_sloth_debug.remote(symbol),             \ 
            open_long.remote(master_api, ACCOUNT_TYPE, symbol, 1),  \
            test_compute_side.remote(symbol, 5),                    \
            test_compute_side.remote(symbol, 5),             \
            close_long.remote(master_api, ACCOUNT_TYPE, symbol, 10), \
            test_compute_side.remote(symbol, 15),             \
            test_compute_side.remote(symbol, 15)              \
            ])         
        
        self.assertEqual(ret2, 0)
        self.assertEqual(ret3, LONG)
        self.assertEqual(ret4, LONG)
        self.assertEqual(ret5, 0)
        self.assertEqual(ret6, OUT)
        self.assertEqual(ret7, OUT)
        ray.shutdown()
    
    # TEST ETH
    def test_long_eth(self):
        # INIT
        symbol = ETHUSDT
        master_api = ApiKeyMaster([API_KEY_MASTER, API_KEY_MASTER_SECRET, OUT, ACCOUNT_TYPE, symbol])
        slave_api = ApiKey([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT)
        ray.init()

        # OPEN LONG + CLOSE LONG
        ret1, ret2, ret3, ret4, ret5, ret6, ret7 = ray.get([ \
            run_winy_sloth_debug.remote(symbol),            \ 
            open_long.remote(master_api, ACCOUNT_TYPE, symbol, 1),  \
            test_compute_side.remote(symbol, 5),            \
            test_compute_side.remote(symbol, 5),            \
            close_long.remote(master_api, ACCOUNT_TYPE, symbol, 10), \
            test_compute_side.remote(symbol, 15),            \
            test_compute_side.remote(symbol, 15)             \
            ])         
        
        self.assertEqual(ret2, 0)
        self.assertEqual(ret3, LONG)
        self.assertEqual(ret4, LONG)
        self.assertEqual(ret5, 0)
        self.assertEqual(ret6, OUT)
        self.assertEqual(ret7, OUT)
        ray.shutdown()
    """
if __name__ == '__main__':
    unittest.main()

#coverage run -m --source=. pytest --junitxml toto.xml tests/tv/spot_tests.py -vxk "not test_compute_side"
#coverage report or coverage html
#coverage run -m pytest tests/tv/spot_tests.py -vxk  "not test_compute_side"; coverage combine; coverage report