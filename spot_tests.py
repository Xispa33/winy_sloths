import os
import subprocess
from time import *
from datetime import *
import unittest
from constant import LONG, SHORT, OUT, BTCUSDT, ETHUSDT
from winy_sloth import WinySloth
from strategy_file import ApiKey, ApiKeyMaster
from password import API_KEY_SLAVE, API_KEY_SLAVE_SECRET

class TestSpot(unittest.TestCase):

    def test_compute_side(self):
        master_api = ApiKeyMaster(["put something here"])
        shell_command = subprocess.run("python3 get_account_info.py --keys " + API_KEY_SLAVE + " " + API_KEY_SLAVE_SECRET + " " + "--type S --symbol " + symbol, shell=True, capture_output=True)
        ret_get_info = shell_command.stdout.decode("utf-8").rstrip('\n')
        pos = WinySloth.WinySloth__ComputeAccountSide(master_api,ret_get_info)
        return pos
        
    def test_open_long(self, symbol):
        shell_command = subprocess.run("python3 open_long.py -k " + API_KEY_SLAVE + " " + API_KEY_SLAVE_SECRET + " " + "-t SPOT -s " + symbol, shell=True, capture_output=True)
        ret_open_long = shell_command.stdout.decode("utf-8").rstrip('\n')
        return ret_open_long

    def test_close_long(self, symbol):
        shell_command = subprocess.run("python3 close_long.py -k " + API_KEY_SLAVE + " " + API_KEY_SLAVE_SECRET + " " + "-t SPOT -s " + symbol, shell=True, capture_output=True)
        ret_close_long = shell_command.stdout.decode("utf-8").rstrip('\n')
        return ret_close_long

    def main_tests(self):
        ret = self.test_compute_side()
        self.assertEqual(ret, OUT)

        # TEST BTC
        ret = self.test_open_long(BTCUSDT)
        self.assertEqual(ret, 0)
        ret = self.test_compute_side()
        self.assertEqual(ret, LONG)

        sleep(2)

        ret = self.test_close_long(BTCUSDT)
        self.assertEqual(ret, 0)
        ret = self.test_compute_side()
        self.assertEqual(ret, OUT)

        sleep(2)

        # TEST ETH
        ret = self.test_open_long(ETHUSDT)
        self.assertEqual(ret, 0)
        ret = self.test_compute_side()
        self.assertEqual(ret, LONG)

        sleep(2)

        ret = self.test_close_long(ETHUSDT)
        self.assertEqual(ret, 0)
        ret = self.test_compute_side()
        self.assertEqual(ret, OUT)

    

if __name__ == '__main__':
    unittest.main()
