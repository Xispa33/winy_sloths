import os
import subprocess
from time import *
from datetime import *
import unittest
from constants import LONG, SHORT, OUT, BTCUSDT, ETHUSDT, SPOT, FUTURES, STOP_MARKET, TYPE, SYMBOL, BNBUSDT
from winy_sloth import WinySloth
from strategy_file import ApiKey, ApiKeyMaster
from password import API_KEY_SLAVE, API_KEY_SLAVE_SECRET
import ast
from binance.client import Client
#python3 -m pytest --junitxml result.xml tests/tu/futures_tests.py -vxk "not test_compute_side"      

def test_compute_side(symbol):
        master_api = ApiKeyMaster([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, FUTURES, symbol])
        shell_command = subprocess.run("python3 ./utils/get_account_info.py --keys " + master_api.api_key + " " + master_api.api_secret_key + " " + "--type F --symbol " + symbol, shell=True, capture_output=True)
        ret_get_info = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        pos = WinySloth.WinySloth__ComputeAccountSide(master_api, ret_get_info)
        return pos

class TestFutures(unittest.TestCase):
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
        master_api = ApiKeyMaster([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, FUTURES, symbol])
        
        # OPEN LONG
        shell_command = subprocess.run("python3 ./utils/open_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t FUTURES -s " + symbol, shell=True, capture_output=True)
        ret_open_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_open_long, 0)
        
        ret = test_compute_side(symbol)
        self.assertEqual(ret, LONG)
        
        sleep(2)
        
        # CLOSE LONG
        shell_command = subprocess.run("python3 ./utils/close_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t FUTURES -s " + symbol, shell=True, capture_output=True)
        ret_close_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_close_long, 0)

        ret = test_compute_side(symbol)
        self.assertEqual(ret, OUT)
    
    # TEST ETH
    def test_long_eth(self):
        # INIT
        symbol = ETHUSDT
        master_api = ApiKeyMaster([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, FUTURES, symbol])
        
        # OPEN LONG
        shell_command = subprocess.run("python3 ./utils/open_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t FUTURES -s " + symbol, shell=True, capture_output=True)
        ret_open_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_open_long, 0)
        
        ret = test_compute_side(symbol)
        self.assertEqual(ret, LONG)
        
        sleep(2)
        
        # CLOSE LONG
        shell_command = subprocess.run("python3 ./utils/close_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t FUTURES -s " + symbol, shell=True, capture_output=True)
        ret_close_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_close_long, 0)

        ret = test_compute_side(symbol)
        self.assertEqual(ret, OUT)

    # TEST BNB
    def test_long_bnb(self):
        # INIT
        symbol = BNBUSDT
        master_api = ApiKeyMaster([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, FUTURES, symbol])
        
        # OPEN LONG
        shell_command = subprocess.run("python3 ./utils/open_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t FUTURES -s " + symbol, shell=True, capture_output=True)
        ret_open_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_open_long, 0)
        
        ret = test_compute_side(symbol)
        self.assertEqual(ret, LONG)
        
        sleep(2)
        
        # CLOSE LONG
        shell_command = subprocess.run("python3 ./utils/close_long.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t FUTURES -s " + symbol, shell=True, capture_output=True)
        ret_close_long = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_close_long, 0)

        ret = test_compute_side(symbol)
        self.assertEqual(ret, OUT)
    
    # TEST BTC
    def test_short_btc(self):
        # INIT
        symbol = BTCUSDT
        master_api = ApiKeyMaster([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, FUTURES, symbol])
        
        # OPEN SHORT
        shell_command = subprocess.run("python3 ./utils/open_short.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t FUTURES -s " + symbol, shell=True, capture_output=True)
        ret_open_short = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_open_short, 0)
        
        ret = test_compute_side(symbol)
        self.assertEqual(ret, SHORT)
        
        sleep(2)
        
        # CLOSE SHORT
        shell_command = subprocess.run("python3 ./utils/close_short.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t FUTURES -s " + symbol, shell=True, capture_output=True)
        ret_close_short = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_close_short, 0)

        ret = test_compute_side(symbol)
        self.assertEqual(ret, OUT)

    # TEST ETH
    def test_short_eth(self):
        # INIT
        symbol = ETHUSDT
        master_api = ApiKeyMaster([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, FUTURES, symbol])
        
        # OPEN SHORT
        shell_command = subprocess.run("python3 ./utils/open_short.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t FUTURES -s " + symbol, shell=True, capture_output=True)
        ret_open_short = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_open_short, 0)
        
        ret = test_compute_side(symbol)
        self.assertEqual(ret, SHORT)
        
        sleep(2)
        
        # CLOSE SHORT
        shell_command = subprocess.run("python3 ./utils/close_short.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t FUTURES -s " + symbol, shell=True, capture_output=True)
        ret_close_short = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_close_short, 0)

        ret = test_compute_side(symbol)
        self.assertEqual(ret, OUT)
    
    # TEST BNB
    def test_short_bnb(self):
        # INIT
        symbol = BNBUSDT
        master_api = ApiKeyMaster([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, FUTURES, symbol])
        
        # OPEN SHORT
        shell_command = subprocess.run("python3 ./utils/open_short.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t FUTURES -s " + symbol, shell=True, capture_output=True)
        ret_open_short = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_open_short, 0)
        
        ret = test_compute_side(symbol)
        self.assertEqual(ret, SHORT)
        
        sleep(2)
        
        # CLOSE SHORT
        shell_command = subprocess.run("python3 ./utils/close_short.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-t FUTURES -s " + symbol, shell=True, capture_output=True)
        ret_close_short = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_close_short, 0)

        ret = test_compute_side(symbol)
        self.assertEqual(ret, OUT)

    """
    # TEST SL BTC
    def test_sl_hedge_btc(self):
        # INIT
        symbol = BTCUSDT
        price = 20000.0
        risk = 0.5
        master_api = ApiKeyMaster([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, FUTURES, symbol])
        client = Client(master_api.api_key, master_api.api_secret_key)
        
        # SET STOP LOSS
        shell_command = subprocess.run("python3 ./utils/set_stop_loss.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-s " + symbol + " -r " + str(risk) + " -p " + str(price) + " -t LONG -m H", shell=True, capture_output=True)
        ret_open_sl = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_open_sl, 0)
        sl_list = client.futures_get_open_orders(symbol=symbol, timestamp=client.futures_time())
 
        self.assertEqual(len(sl_list), 1)
        self.assertEqual(sl_list[0][SYMBOL], symbol)
        self.assertEqual(sl_list[0][TYPE], STOP_MARKET)
        self.assertEqual(sl_list[0]['stopPrice'], str(int(price*risk)))
        
        sleep(2)

        # CLEAR STOP LOSS
        shell_command = subprocess.run("python3 ./utils/clear_stop_loss.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-s " + symbol, shell=True, capture_output=True)
        ret_close_sl = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_close_sl, 0)
        sl_list = client.futures_get_open_orders(symbol=symbol, timestamp=client.futures_time())
 
        self.assertEqual(len(sl_list), 0)
    
    # TEST SL ETH
    def test_sl_hedge_eth(self):
        # INIT
        symbol = ETHUSDT
        price = 500.0
        master_api = ApiKeyMaster([API_KEY_SLAVE, API_KEY_SLAVE_SECRET, OUT, FUTURES, symbol])
        client = Client(master_api.api_key, master_api.api_secret_key)
        
        # SET STOP LOSS
        shell_command = subprocess.run("python3 ./utils/set_stop_loss.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-s " + symbol + " -r " + str(0) + " -p " + str(price) + " -t LONG -m H", shell=True, capture_output=True)
        ret_open_sl = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_open_sl, 0)
        sl_list = client.futures_get_open_orders(symbol=symbol, timestamp=client.futures_time())
 
        self.assertEqual(len(sl_list), 1)
        self.assertEqual(sl_list[0][SYMBOL], symbol)
        self.assertEqual(sl_list[0][TYPE], STOP_MARKET)
        self.assertEqual(sl_list[0]['stopPrice'], str(int(price)))
        
        sleep(2)

        # CLEAR STOP LOSS
        shell_command = subprocess.run("python3 ./utils/clear_stop_loss.py -k " + master_api.api_key + " " + master_api.api_secret_key + " " + "-s " + symbol, shell=True, capture_output=True)
        ret_close_sl = ast.literal_eval(shell_command.stdout.decode("utf-8").rstrip('\n'))
        self.assertEqual(ret_close_sl, 0)
        sl_list = client.futures_get_open_orders(symbol=symbol, timestamp=client.futures_time())
 
        self.assertEqual(len(sl_list), 0)
    """
if __name__ == '__main__':
    unittest.main()
