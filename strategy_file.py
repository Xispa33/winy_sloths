#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from binance.client import Client
from interface_binance import *
from header import *
from history import *
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

class ApiKeySlave(ApiKey):
    def __init__(self, info_strategy_file):
        super().__init__(info_strategy_file)
    
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