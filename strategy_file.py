#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from binance.client import Client
from interface_binance import *
from constants import *
from errors import *

class ApiKey:
    def __init__(self, info_strategy_file):
        self.api_key = info_strategy_file[0]
        self.api_secret_key = info_strategy_file[1]
        self.side = info_strategy_file[2]


class ApiKeyMaster(ApiKey):
    def __init__(self, info_strategy_file):
        super().__init__(info_strategy_file)
        self.account_type = info_strategy_file[3]
        self.symbol = info_strategy_file[4]
        self.markPrice = 0
        self.entryPrice = 0
        self.leverage = 0
        self.positionAmt = 0
        self.engaged_balance = 0
        self.balance = 0
    
    def computeEngagedBalance(self):
        self.engaged_balance = (self.positionAmt *self.entryPrice/self.balance)

class ApiKeySlave(ApiKey):
    def __init__(self, info_strategy_file):
        super().__init__(info_strategy_file)

    def close_long(self, master_api):
        client = Client(self.api_key, self.api_secret_key)
        return I__CLOSE_LONG(client, master_api)

    def close_short(self, master_api):
        client = Client(self.api_key, self.api_secret_key)
        return I__CLOSE_SHORT(client, master_api)

    def open_long(self, master_api):
        client = Client(self.api_key, self.api_secret_key)
        return I__OPEN_LONG(client, master_api)

    def open_short(self, master_api):
        client = Client(self.api_key, self.api_secret_key)
        return I__OPEN_SHORT(client, master_api)
    
    def open_long_from_short(self, master_api):
        if (not self.close_short(master_api)):
            return self.open_long(master_api)
        else:
            return 1

    def open_short_from_long(self, master_api):
        if (not self.close_long(master_api)):
            return self.open_short(master_api)
        else:
            return 1
    
class StrategyFile:
    def __init__(self, strategy_file_path, info_strategy_file_master, info_strategy_file_slave):
        self.strategy_file_path = strategy_file_path
        self.master_api = ApiKeyMaster(info_strategy_file_master)
        self.slave_apis = self.StrategyFile__InitSlaves(info_strategy_file_slave)
        self.global_slave_status = 0

    def StrategyFile__InitSlaves(self, info_strategy_file_slave):
        slaves_list = []

        for slaves in info_strategy_file_slave:
            slaves_list.append(ApiKeySlave(slaves.strip('\n').split(" ")))

        return slaves_list