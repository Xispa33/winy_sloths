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
import ray

#python3 -m pytest --junitxml result.xml tests/tu/spot_tests.py -vxk "not test_compute_side"      

PATH = "tests/tv/TEST_FUTURES/"
ACCOUNT_TYPE = FUTURES

@ray.remote
def test_compute_side(account, symbol, wait):
        sleep(wait)
        shell_command = subprocess.run("python3 ./utils/get_account_info.py --keys " + account.api_key + " " + account.api_secret_key + " " + "--type S --symbol " + symbol, shell=True, capture_output=True)
        ret_get_info = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        pos = WinySloth.WinySloth__ComputeAccountSide(account, ret_get_info)
        return pos

@ray.remote
def run_winy_sloth_debug(symbol):
    subprocess.run("python3 --mode debug --folder " + PATH + \
                   "/TEST_OUT_" + symbol + " main.py", shell=True, capture_output=True)

@ray.remote
def open_long(master_api, account_type, symbol, wait):
    sleep(wait)
    shell_command = subprocess.run("python3 ./utils/open_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t " + account_type + " -s " + symbol, shell=True, capture_output=True)
    ret_open_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
    return ret_open_long

@ray.remote
def close_long(master_api, account_type, symbol, wait):
    sleep(wait)
    shell_command = subprocess.run("python3 ./utils/close_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t " + account_type " -s " + symbol, shell=True, capture_output=True)
    ret_close_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
    return ret_close_long

class TestSpot(unittest.TestCase):
    def test_eth_out(self):
        ray.init()

        symbol = ETHUSDT
        master_api = ApiKeyMaster([API_MASTER_SLAVE, API_KEY_MASTER_SECRET, OUT, ACCOUNT_TYPE, symbol])
        
        ret1, ret2 = ray.get([run_winy_sloth_debug.remote(symbol), \
                              test_compute_side.remote(master_api, symbol, 10)])
        self.assertEqual(ret2, OUT)
        
        ray.shutdown()
    
    def test_btc_out(self):
        ray.init()
        
        symbol = BTCUSDT
        master_api = ApiKeyMaster([API_KEY_MASTER, API_KEY_MASTER_SECRET, OUT, ACCOUNT_TYPE, symbol])
        
        ret1, ret2 = ray.get([run_winy_sloth_debug.remote(symbol), \
                              test_compute_side.remote(master_api, symbol, 10)])
        self.assertEqual(ret2, OUT)

        ray.shutdown()
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
            open_long.remote(master_api, ACCOUNT_TYPE, symbol, 1), \
            test_compute_side.remote(symbol, 5),                   \
            test_compute_side.remote(symbol, 5),                   \
            close_long.remote(master_api, ACCOUNT_TYPE, symbol, 10), \
            test_compute_side.remote(symbol, 15),                    \
            test_compute_side.remote(symbol, 15)                     \
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
            run_winy_sloth_debug.remote(symbol),             \ 
            open_long.remote(master_api, ACCOUNT_TYPE, symbol, 1), \
            test_compute_side.remote(symbol, 5),                   \
            test_compute_side.remote(symbol, 5),                   \
            close_long.remote(master_api, ACCOUNT_TYPE, symbol, 10), \
            test_compute_side.remote(symbol, 15),                    \
            test_compute_side.remote(symbol, 15)                     \
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

#Ajouter open short, close short
# Check Stop loss 