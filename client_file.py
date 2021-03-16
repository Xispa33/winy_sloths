#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from binance.client import Client
from interface_binance import *
from header import *
from history import *
from constants import *

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
        self.return_tuple     = (1,1,1,1) #(check_filepath, read_file_return, check_file_header_return, check_file_keys_return)
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
    
    def return_transaction(self, strategy_history, transaction_idx):
        #type | time | id | orderId | symbol | symbol_price | side | quantity | realized_pnl | current_side
        if (self.header.key_list[transaction_idx].account_type == FUTURES):
            dict_keys_list = ['type', 'time', 'id', 'orderId', 'symbol', 'price', 'side', 'qty', 'realizedPnl', 'current_side']
            strategy_history_dict = {dict_keys_list[i]:strategy_history[i] for i in range(0, len(dict_keys_list))}
            return (TransactionFutures(strategy_history_dict, Client(self.header.key_list[transaction_idx].api_key, self.header.key_list[transaction_idx].api_secret_key)))
        elif (self.header.key_list[transaction_idx].account_type == SPOT):
            dict_keys_list = ['type', 'time', 'orderId', 'symbol', 'price', 'side', 'origQty', 'current_side']
            strategy_history_dict = {dict_keys_list[i]:strategy_history[i] for i in range(0, len(dict_keys_list))}
            return (TransactionSpot(strategy_history_dict))
        else:
            return 1
    
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
                        account_type = info[2+i].split()[2]
                        self.header.key_list.append(ApiKeyClass(i,api_key,api_code_key, NOT_VALID_KEY, account_type))
                        self.header.cpt_strategies +=1
                    
                #read history
                for transaction_idx in range(0,self.header.all_strategies_nb):
                    strategy_history = info[2+self.header.all_strategies_nb+transaction_idx+1].rstrip('\n').split(';')
                    
                    last_transaction = self.return_transaction(strategy_history, transaction_idx)
                    
                    #last_transaction = Transaction(strategy_history)
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

        self.return_tuple = (self.check_filepath(), self.read_file(), self.header.check_header(), self.header.check_keys_list())
        if ( (self.return_tuple[0] != 0) or (self.return_tuple[1] != 0) or (self.return_tuple[2] != 0) or (self.return_tuple[3] != 0)):
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
                for transaction_idx in range(0,self.header.all_strategies_nb):
                    strategy_history = info[2+self.header.all_strategies_nb+transaction_idx+1].rstrip('\n').split(';')
                    last_transaction = self.return_transaction(strategy_history, transaction_idx)
                    print(last_transaction)
                    self.history.history_list.append(last_transaction)
                txt_file.close()
            return 0
        except:
            return 1

    def write_file_history(self, strategy_idx, last_trade):
        try:
            with open(self.client_file_path, 'r') as txt_file:
                info = txt_file.readlines()
                
                txt_file.close()

            with open(self.client_file_path, 'w') as txt_file:
                info[2+self.header.all_strategies_nb+(strategy_idx)+1] = str(last_trade)
                txt_file.writelines(info)   
                txt_file.close()
        
            return 0
        except:
            return 1
    
    def is_strategy_idx_valid(self, strategy_idx):
        for key in self.header.key_list:
            if key.strategy_idx == strategy_idx:
                return True
        return False

    def find_strategy_api_key(self, strategy_idx):
        if (self.is_strategy_idx_valid(strategy_idx)):
            for key in self.header.key_list:
                if key.strategy_idx == strategy_idx:
                    return (key)
        else:
            return 1

    def get_futures_trade(self, strategy_idx):
        api_key = self.find_strategy_api_key(strategy_idx)
        client = Client(api_key.api_key, api_key.api_secret_key)
        if (api_key.api_validity == VALID_KEY):
            #transaction_list = I__GET_ACCOUNT_HISTORY(client, api_key.account_type, self.history.history_list[strategy_idx].symbol)
            if api_key.account_type == FUTURES:
                #Futures account example
                transaction_list = [{'symbol': 'ETHUSDT', 'id': 384187499, 'orderId': 8389765493651748878, 'side': 'SELL', 'price': '1535.45', 'qty': '1.474', 'realizedPnl': '0', 'marginAsset': 'USDT', 'quoteQty': '2263.25330', 'commission': '0.45265066', 'commissionAsset': 'USDT', 'time': 1614974810111, 'positionSide': 'BOTH', 'maker': True, 'buyer': False}, {'symbol': 'ETHUSDT', 'id': 384498527, 'orderId': 8389765493659577085, 'side': 'BUY', 'price': '1546.11', 'qty': '1.474', 'realizedPnl': '-15.71284000', 'marginAsset': 'USDT', 'quoteQty': '2278.96614', 'commission': '0.45579322', 'commissionAsset': 'USDT', 'time': 1614991360231, 'positionSide': 'BOTH', 'maker': True, 'buyer': True}, {'symbol': 'ETHUSDT', 'id': 386113569, 'orderId': 8389765493693917332, 'side': 'BUY', 'price': '1636.07', 'qty': '1.386', 'realizedPnl': '0', 'marginAsset': 'USDT', 'quoteQty': '2267.59302', 'commission': '0.45351860', 'commissionAsset': 'USDT', 'time': 1615061346339, 'positionSide': 'BOTH', 'maker': True, 'buyer': True}]
            else:
                #Spot account example
                transaction_list = [{'symbol': 'BTCUSDT', 'orderId': 5211308012, 'orderListId': -1, 'clientOrderId': 'x-K309V22B-km7ojj23ybr0kzjtq6m', 'price': '59800.76000000', 'origQty': '0.02100000', 'executedQty': '0.02100000', 'cummulativeQuoteQty': '1255.81596000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1615636978951, 'updateTime': 1615637009689, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}]
        else:
            return 1

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
            
            if (self.header.key_list[strategy_idx].account_type == FUTURES):
                return (convert_raw_trade_to_transaction(ret_last_futures_read))
            elif (self.header.key_list[strategy_idx].account_type == SPOT):
                return (convert_raw_trade_to_transaction(ret_last_futures_read))
            else:
                return 1
    
    def ClientFile__GetFileHistory(self):
        return (self.read_file_history())
    
    def ClientFile__GetStrategyHistory(self, strategy_idx):
        return (self.history.history_list[strategy_idx])

    # Ici, on compare l'historique d'une stratégie de l'objet avec l'historique passé en paramètre
    def ClientFile__CompareStrategy(self, strategy_idx, last_trade):
        #return (self.history.history_list[strategy_idx] == last_trade.history.history_list[strategy_idx])
        return (self.history.history_list[strategy_idx] == last_trade)

    def ClientFile__Act(self, strategy_history, last_trade):
        #ecriture dans le fichier .txt
        #ClientFile__ReadHistory
        write_ret = 1
        update_ret = 1

        write_ret = self.write_file_history(strategy_history, last_trade)
        update_ret = self.read_file_history()

        if ((write_ret == 1) or (update_ret == 1)):
            return 1
        else:
            return 0

def convert_raw_trade_to_transaction(raw_trade):
        # time | id | orderId | symbol | symbol_price | side | quantity | realized_pnl
        if isinstance(raw_trade, dict):
            if 'realizedPnl' in raw_trade:
                """ Futures transaction """
                return TransactionFutures(raw_trade, None)
            else:
                """ Spot transaction """
                #[{'symbol': 'BTCUSDT', 'orderId': 5211308012, 'orderListId': -1, 'clientOrderId': 'x-K309V22B-km7ojj23ybr0kzjtq6m', 'price': '59800.76000000', 'origQty': '0.02100000', 'executedQty': '0.02100000', 'cummulativeQuoteQty': '1255.81596000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1615636978951, 'updateTime': 1615637009689, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}]
                return TransactionSpot(raw_trade)
        else:
            return 1

def run(tree):
    for strategy_idx in range(0,tree.header.nb_keys):
        #READ FUTURES HISTORY
        file_last_trade = tree.ClientFile__GetStrategyHistory(strategy_idx)
        future_last_trade_binance = tree.ClientFile__GetBinanceHistory(strategy_idx)
        
        #COMPARE WITH CURRENT
        if (type(future_last_trade_binance) == type(file_last_trade)):
            if not future_last_trade_binance == file_last_trade:
                #ACT = MAJ fichier .txt + MAJ historique de l'objet
                tree.ClientFile__Act(strategy_idx, future_last_trade_binance)
                # LECTURE FICHIER TXT APRES MODIF : DEJA FAIT DANS ClientFile__Act
                #tree.ClientFile__GetFileHistory()
            else:
                print("SAME HISTORY\n")
        else:
            return 1
