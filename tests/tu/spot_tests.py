import os
import subprocess
from time import *
from datetime import *
import unittest
from constants import LONG, SHORT, OUT, BTCUSDT, ETHUSDT, SPOT, FUTURES, BNBUSDT
from winy_sloth import WinySloth
from strategy_file import ApiKey, ApiKeyMaster
from password import API_KEY_SLAVE, API_KEY_SLAVE_SECRET, API_KEY_MASTER, API_KEY_MASTER_SECRET
import ast
#python3 -m pytest --junitxml result.xml tests/tu/spot_tests.py -vxk "not test_compute_side"      


def test_compute_side(symbol):
        master_api = ApiKeyMaster([API_KEY_MASTER, API_KEY_MASTER_SECRET, OUT, SPOT, symbol])
        shell_command = subprocess.run("python3 ./utils/get_account_info.py --keys " + master_api.api_key + " " + master_api.api_secret_key + " " + "--type S --symbol " + symbol, shell=True, capture_output=True)
        ret_get_info = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        pos = WinySloth.WinySloth__ComputeAccountSide(master_api, ret_get_info)
        return pos

class TestSpot(unittest.TestCase):
    def test_eth_out(self):
        ret = test_compute_side(ETHUSDT)
        self.assertEqual(ret, OUT)
    
    def test_btc_out(self):
        ret = test_compute_side(BTCUSDT)
        self.assertEqual(ret, OUT)
    
    def test_bnb_out(self):
        ret = test_compute_side(BNBUSDT)
        self.assertEqual(ret, OUT)
    
    # TEST BTC
    def test_long_btc(self):
        # INIT
        symbol = BTCUSDT
        master_api = ApiKeyMaster([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, SPOT, symbol])
        
        # OPEN LONG
        shell_command = subprocess.run("python3 ./utils/open_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t SPOT -s " + symbol, shell=True, capture_output=True)
        ret_open_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_open_long, 0)
        
        ret = test_compute_side(symbol)
        self.assertEqual(ret, LONG)
        
        sleep(2)
        
        # CLOSE LONG
        shell_command = subprocess.run("python3 ./utils/close_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t SPOT -s " + symbol, shell=True, capture_output=True)
        ret_close_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_close_long, 0)

        ret = test_compute_side(symbol)
        self.assertEqual(ret, OUT)

    # TEST ETH
    def test_long_eth(self):
        # INIT
        symbol = ETHUSDT
        master_api = ApiKeyMaster([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, SPOT, symbol])
        
        # OPEN LONG
        shell_command = subprocess.run("python3 ./utils/open_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t SPOT -s " + symbol, shell=True, capture_output=True)
        ret_open_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_open_long, 0)
        
        ret = test_compute_side(symbol)
        self.assertEqual(ret, LONG)
        
        sleep(2)
        
        # CLOSE LONG
        shell_command = subprocess.run("python3 ./utils/close_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t SPOT -s " + symbol, shell=True, capture_output=True)
        ret_close_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_close_long, 0)

        ret = test_compute_side(symbol)
        self.assertEqual(ret, OUT)
    
    # TEST BNB
    def test_long_bnb(self):
        # INIT
        symbol = BNBUSDT
        master_api = ApiKeyMaster([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, SPOT, symbol])
        
        # OPEN LONG
        shell_command = subprocess.run("python3 ./utils/open_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t SPOT -s " + symbol, shell=True, capture_output=True)
        ret_open_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_open_long, 0)
        
        ret = test_compute_side(symbol)
        self.assertEqual(ret, LONG)
        
        sleep(2)
        
        # CLOSE LONG
        shell_command = subprocess.run("python3 ./utils/close_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t SPOT -s " + symbol, shell=True, capture_output=True)
        ret_close_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_close_long, 0)

        ret = test_compute_side(symbol)
        self.assertEqual(ret, OUT)
    
if __name__ == '__main__':
    unittest.main()
