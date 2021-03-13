#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from binance.client import Client
from interface_binance import *
from header import *
from history import *

class ClientFile:
    """
    A class used to represent the client's file

    Attributes
    ----------
    client_file_path : list
        List of the last 5 trades made for each and every API key

    header : Header
        List of the last 5 trades made for each and every API key
    
    history : History
        List of the last 5 trades made for each and every API key
    
    init_status : list
        List of the last 5 trades made for each and every API key

    Methods
    -------
    
    """
    def __init__(self, client_file):
        self.client_file_path = client_file
        self.header           = Header()
        self.history          = History()
        self.return_tuple     = (1,1,1,1,1) #(check_filepath, read_file_return, check_file_header_return, check_file_keys_return, check_file_history_return)
        self.init_status      = self.ClientFile__Init()

    def __repr__(self):
        #TODO: A modifier pour que l'affichage soit automatique
        out = str()
        out += "client_file_path = {}\n".format(self.client_file_path)
        out += self.header.__repr__()
        #out += self.history.__repr__()
        out += "return_tuple = {}\n".format(str(self.return_tuple))
        out += "init_status = {}\n".format(self.init_status)

        return (out)
    
    def read_file(self):
        cpt_strategies = 0
        try:
            with open(self.client_file_path, 'r') as txt_file:
                info = txt_file.readlines()
                #read header
                self.header.client_name = info[0].rstrip('\n')
                self.header.nb_keys = int(info[1].rstrip('\n'))
                for i in range(0,self.header.all_strategies_nb):
                    key_pair = info[2+i].rstrip('\n')
                    if key_pair != "NA":
                        api_key = info[2+i].split()[0]
                        api_code_key = info[2+i].split()[1]
                        self.header.key_list.append(ApiKeyClass(i,api_key,api_code_key, 0))
                        self.header.cpt_strategies +=1
                    
                #read history
                for i in range(0,self.header.all_strategies_nb):
                    strategy_history = info[2+self.header.all_strategies_nb+i+1].rstrip('\n').split(';')
                    last_transaction = Transaction(strategy_history)
                    print(last_transaction)
                    self.history.history_list.append(last_transaction)
                    #print(strategy_history)
                    
                txt_file.close()
                    
            return 0
                
        except:
            return 1 

    def check_filepath(self):
        if os.path.exists(self.client_file_path):
            return 0
        else:
            return 1
        
    def ClientFile__Init(self):
        #(read_file_return, check_file_header_return, check_file_keys_return, check_file_history_return)
        #self.check_header_keys()

        self.return_tuple = (self.check_filepath(), self.read_file(), self.header.check_header(), self.header.check_keys_list(), self.history.check_history())
        if ( (self.return_tuple[0] != 0) or (self.return_tuple[1] != 0) or (self.return_tuple[2] != 0) or (self.return_tuple[3] != 0) or (self.return_tuple[4] != 0)):
            #send mail 
            #TODO ici, si jamais une clé est mauvaise, il faut envoyer un mail avec le nombre de clé mauvaises et les stratégies correspondantes
            print("KO")
            return 1
        else:
            print("OK")
            return 0

    def read_file_history(self):
        self.history.clear()
        try:
            with open(self.client_file_path, 'r') as txt_file:
                info = txt_file.readlines()    
                #read history
                for i in range(0,self.header.all_strategies_nb):
                    strategy_history = info[2+self.header.all_strategies_nb+i+1].rstrip('\n').split(';')
                    last_transaction = Transaction(strategy_history)
                    print(last_transaction)
                    self.history.history_list.append(last_transaction)
                    #print(strategy_history)
                        
                txt_file.close()
            return 0
        except:
            return 1

    def ClientFile__WriteHistory(self):
        self.history.clear()
        with open(self.client_file_path, 'rw') as txt_file:
            info = txt_file.readlines()    
            #read history
            for i in range(0,self.header.all_strategies_nb):
                strategy_history = info[2+self.header.all_strategies_nb+i+1].rstrip('\n').split(';')
                last_transaction = Transaction(strategy_history)
                print(last_transaction)
                #self.history.history_list.append(last_transaction)
                #print(strategy_history)
                    
            txt_file.close()
    
    def is_strategy_idx_valid(self, strategy_idx):
        for key in self.header.key_list:
            if key.strategy_idx == strategy_idx:
                return True
        return False

    def find_strategy_api_key(self, strategy_idx):
        if (self.is_strategy_idx_valid(strategy_idx)):
            for key in self.header.key_list:
                if key.strategy_idx == strategy_idx:
                    return (key.api_key, key.api_secret_key)
        else:
            return 1

    def get_futures_trade(self, strategy_idx):
        credentials = self.find_strategy_api_key(strategy_idx)
        client = Client(credentials[0], credentials[1])
        #transaction_list = I__FUTURES_ACCOUNT_TRADES(client)
        transaction_list = [{'symbol': 'ETHUSDT', 'id': 384187499, 'orderId': 8389765493651748878, 'side': 'SELL', 'price': '1535.45', 'qty': '1.474', 'realizedPnl': '0', 'marginAsset': 'USDT', 'quoteQty': '2263.25330', 'commission': '0.45265066', 'commissionAsset': 'USDT', 'time': 1614974810111, 'positionSide': 'BOTH', 'maker': True, 'buyer': False}, {'symbol': 'ETHUSDT', 'id': 384498527, 'orderId': 8389765493659577085, 'side': 'BUY', 'price': '1546.11', 'qty': '1.474', 'realizedPnl': '-15.71284000', 'marginAsset': 'USDT', 'quoteQty': '2278.96614', 'commission': '0.45579322', 'commissionAsset': 'USDT', 'time': 1614991360231, 'positionSide': 'BOTH', 'maker': True, 'buyer': True}, {'symbol': 'ETHUSDT', 'id': 386113569, 'orderId': 8389765493693917332, 'side': 'BUY', 'price': '1636.07', 'qty': '1.386', 'realizedPnl': '0', 'marginAsset': 'USDT', 'quoteQty': '2267.59302', 'commission': '0.45351860', 'commissionAsset': 'USDT', 'time': 1615061346339, 'positionSide': 'BOTH', 'maker': True, 'buyer': True}]

        if (transaction_list != 1):
            return transaction_list
        else:
            return 1

    def get_last_futures_trade(self, transaction_list):
        if (transaction_list != 1):
            return transaction_list[-1]
        else:
            return 1

    def ClientFile__GetBinanceHistory(self, strategy_idx):
        
        ret_last_futures_read = 1

        ret_last_futures_read = self.get_last_futures_trade(self.get_futures_trade(strategy_idx))

        if (isinstance(ret_last_futures_read, int)):
            return 1
        else:
            return (convert_raw_trade_to_transaction(ret_last_futures_read))
    
    def ClientFile__GetFileHistory(self):
        return self.read_file_history()
    
    def ClientFile__GetStrategyHistory(self, strategy_idx):
        return (self.history.history_list[strategy_idx-1])

    # Ici, on compare l'historique d'une stratégie de l'objet avec l'historique passé en paramètre
    def ClientFile__CompareStrategy(self, strategy_idx, last_trade):
        #return (self.history.history_list[strategy_idx-1] == last_trade.history.history_list[strategy_idx-1])
        return (self.history.history_list[strategy_idx-1] == last_trade)

    def ClientFile__Act(self):
        #ecriture dans le fichier .txt
        #ClientFile__ReadHistory
        print("toto")

def convert_raw_trade_to_transaction(raw_trade):
        #(time, id, orderId, symbol, symbol_price, initial_side, side, new_side, quantity, realized_pnl)
        transaction = [raw_trade['time'], raw_trade['id'],raw_trade['orderId'], raw_trade['symbol'], raw_trade['price'], \
        "NEUTRE", raw_trade['side'], "NEUTRE", raw_trade['qty'], raw_trade['realizedPnl']]

        return Transaction(transaction)

def run(tree):
        strategy_idx = 1
        tree.ClientFile__GetFileHistory()
        #READ FUTURE HISTORY
        file_last_trade = tree.ClientFile__GetStrategyHistory(strategy_idx)
        future_last_trade_binance = tree.ClientFile__GetBinanceHistory(strategy_idx)
        
        #COMPARE WITH CURRENT
        if (isinstance(future_last_trade_binance, Transaction) and isinstance(file_last_trade, Transaction)): 
            if not future_last_trade_binance == file_last_trade:
                #ACT = MAJ fichier .txt + MAJ historique de l'objet
                tree.ClientFile__Act()
                print("DIFFERENT HISTORY\n")
            else:
                print("SAME HISTORY\n")
        else:
            return 1
