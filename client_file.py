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
        self.return_tuple     = (1,1)
        self.errors           = Errors()
        self.init_status      = self.ClientFile__Init()
        if (self.init_status):
            Errors.Errors__SendEmail(self.errors)
            sys.exit()

    def __repr__(self):
        out = str()
        out += "client_file_path = {}\n".format(self.client_file_path)
        out += self.header.__repr__()
        out += "return_tuple = {} (check_filepath() return, read_file() return, check_file_header() return, check_file_keys() return) \n".format(str(self.return_tuple))
        out += "init_status = {}\n".format(self.init_status)
        #out += self.error_messages
        return (out)
    
    def return_transaction(self, strategy_history, transaction_idx):
        return Transaction.create_transaction(self.header.key_list[transaction_idx].account_type, \
                                                   strategy_history, \
                                                   Client(self.header.key_list[transaction_idx].api_key, \
                                                          self.header.key_list[transaction_idx].api_secret_key))

    def read_file(self):
        cpt_strategies = 0
        FUNCTION = "read_file()"
        ret = 0
        try:
            with open(self.client_file_path, 'r') as txt_file:
                info = txt_file.readlines()
                #read header
                self.header.client_name = info[0].rstrip('\n')
                self.header.nb_keys = int(info[1].rstrip('\n'))
                for i in range(0,self.header.all_strategies_nb):
                    key_pair = info[2+i].rstrip('\n')
                    if key_pair != NA:
                        api_key = info[2+i].split()[0]
                        api_code_key = info[2+i].split()[1]
                        account_type = info[2+i].split()[2]
                        self.header.key_list.append(ApiKeyClass(i,api_key,api_code_key, NOT_VALID_KEY, account_type))
                        self.header.cpt_strategies +=1
                
                self.errors = Errors.Errors__Init(self.header.all_strategies_nb) 

                #read history
                for transaction_idx in range(0,self.header.all_strategies_nb):
                    strategy_history = info[2+self.header.all_strategies_nb+transaction_idx+1].rstrip('\n').split(';')
                    try:
                        last_transaction = self.return_transaction(strategy_history, transaction_idx)
                        self.history.add_transaction(last_transaction)
                        print(repr(last_transaction))
                    except:
                        self.errors.Errors__FillErrors(FUNCTION, Errors.Errors__GetRawExceptionInfo(sys.exc_info()) + \
                            "This error message occured for strategy {}. \n".format(transaction_idx), HIGH_C)
                        ret = 1
                txt_file.close()
            
            return ret
        except:
            self.errors.Errors__FillErrors(FUNCTION, Errors.Errors__GetRawExceptionInfo(sys.exc_info()), HIGH_C)
            return 1 

    def check_filepath(self):
        FUNCTION = "check_filepath()"
        if os.path.exists(self.client_file_path):
            return 0
        else:
            self.errors.Errors__FillErrors(FUNCTION, "Path : " + self.client_file_path + " does not exist !\n", HIGH_C)
            return 1
        
    def ClientFile__Init(self):
        self.return_tuple = (self.check_filepath(), self.header.check_keys_list(self.header.check_header(self.read_file(), self.errors), self.errors))
        
        if (self.return_tuple != (0, 0)):
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
                    print(repr(last_transaction))
                    self.history.add_transaction(last_transaction)
                    #self.history.history_list.append(last_transaction)
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
        FUNCTION = "get_futures_trade()"
        api_key = self.find_strategy_api_key(strategy_idx)
        if (api_key != 1):
            client = Client(api_key.api_key, api_key.api_secret_key)
            if (api_key.api_validity == VALID_KEY):
                transaction_list = I__GET_ACCOUNT_HISTORY(client, api_key.account_type, self.history[strategy_idx].symbol)
                """
                if api_key.account_type == FUTURES:
                    #Futures account example
                    transaction_list = [{'symbol': 'ETHUSDT', 'id': 384187499, 'orderId': 8389765493651748878, 'side': 'SELL', 'price': '1535.45', 'qty': '1.474', 'realizedPnl': '0', 'marginAsset': 'USDT', 'quoteQty': '2263.25330', 'commission': '0.45265066', 'commissionAsset': 'USDT', 'time': 1614974810111, 'positionSide': 'BOTH', 'maker': True, 'buyer': False}, {'symbol': 'ETHUSDT', 'id': 384498527, 'orderId': 8389765493659577085, 'side': 'BUY', 'price': '1546.11', 'qty': '1.474', 'realizedPnl': '-15.71284000', 'marginAsset': 'USDT', 'quoteQty': '2278.96614', 'commission': '0.45579322', 'commissionAsset': 'USDT', 'time': 1614991360231, 'positionSide': 'BOTH', 'maker': True, 'buyer': True}, {'symbol': 'ETHUSDT', 'id': 386113569, 'orderId': 8389765493693917332, 'side': 'BUY', 'price': '1636.07', 'qty': '1.386', 'realizedPnl': '0', 'marginAsset': 'USDT', 'quoteQty': '2267.59302', 'commission': '0.45351860', 'commissionAsset': 'USDT', 'time': 1615061346339, 'positionSide': 'BOTH', 'maker': True, 'buyer': True}]
                else:
                    #Spot account example
                    transaction_list = [{'symbol': 'BTCUSDT', 'orderId': 5211308012, 'orderListId': -1, 'clientOrderId': 'x-K309V22B-km7ojj23ybr0kzjtq6m', 'price': '59800.76000000', 'origQty': '0.02100000', 'executedQty': '0.02100000', 'cummulativeQuoteQty': '1255.81596000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1615636978951, 'updateTime': 1615637009689, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}]
                """ 
            if (transaction_list != 1):
                return transaction_list
            else:
                return 1
        else:
            self.errors.Errors__FillErrors(FUNCTION, "Strategy index : " + strategy_idx + " was not found among the existing strategies index !\n", MEDIUM_C)
            return 1

            

    def get_last_futures_trade(self, transaction_list):
        if (transaction_list != 1):
            return transaction_list[-1]
        else:
            return 1
    
    def ClientFile__GetBinanceHistory(self, strategy_idx):
        #TODO: Mettre peut etre un retry pour tester les datas recues
        FUNCTION = "ClientFile__GetBinanceHistory()"
        ret_last_futures_read = 1

        ret_last_futures_read = self.get_last_futures_trade(self.get_futures_trade(strategy_idx))

        if (isinstance(ret_last_futures_read, int)):
            self.errors.Errors__FillErrors(FUNCTION, "Strategy index : " + strategy_idx + " failed to retrieve information from Binance !\n", MEDIUM_C)
            self.header.key_list[strategy_idx].api_validity = NOT_VALID_KEY
            return 1
        else:
            if (self.header.key_list[strategy_idx].account_type == FUTURES) or (self.header.key_list[strategy_idx].account_type == SPOT):
                return (Transaction.convert_raw_trade_to_transaction(ret_last_futures_read, Client(self.header.key_list[strategy_idx].api_key, self.header.key_list[strategy_idx].api_secret_key)))
            else:
                self.errors.Errors__FillErrors(FUNCTION, "Strategy index : " + strategy_idx + " transaction information retrieved from Binance is incorrect !\n", MEDIUM_C)
                self.header.key_list[strategy_idx].api_validity = NOT_VALID_KEY
                return 1
    
    def ClientFile__GetFileHistory(self):
        return (self.read_file_history())
    
    def ClientFile__ModifyClientFileHistory(self, strategy_history, last_trade):
        return (self.write_file_history(strategy_history, last_trade))
    
    def ClientFile__GetStrategyHistory(self, strategy_idx):
        return (self.history.history_list[strategy_idx])

    def ClientFile__UpdateHistory(self, strategy_history, last_trade):
        FUNCTION = "ClientFile__UpdateHistory"
        write_ret = 1
        update_ret = 1
        #Check ici
        write_ret = self.ClientFile__ModifyClientFileHistory(strategy_history, last_trade)
        update_ret = self.ClientFile__GetFileHistory()

        if ((write_ret == 1) or (update_ret == 1)):
            return 1 
        else: 
            self.errors.Errors__FillErrors(FUNCTION, "Strategies changed !!!!!\n", INFO_C)
            Errors.Errors__SendEmail(self.errors)
            return 0

    def ClientFile__CheckErrors(self):
        cpt_err = 0
        for i in range(self.header.all_strategies_nb):
            if (self.errors.mail_sent[i] == 0 and self.header.key_list[i].api_validity == NOT_VALID_KEY):
                Errors.Errors__SendEmail(self.errors)
                self.errors.mail_sent[i] = 1
                
            if self.errors.mail_sent[i] == 1:
                cpt_err += 1

        if (cpt_err > MAX_KO_STRATEGY):
            self.errors.Errors__FillErrors(FUNCTION, "Too many strategies are KO. See previous mails. Program ended unexpectedly !!!!!\n", HIGH_C)
            Errors.Errors__SendEmail(self.errors)
            sys.exit()

        self.errors.error_messages = ""
        self.errors.err_criticity = INFO_C


def run(tree):
    for strategy_idx in range(0,tree.header.nb_keys):
        """ Check if API key is valid """
        if (tree.header.key_list[strategy_idx].api_validity == VALID_KEY):
            """ READ HISTORY IN CLIENT FILE """
            file_last_trade = tree.ClientFile__GetStrategyHistory(strategy_idx)
            """ READ HISTORY IN BINANCE """
            future_last_trade_binance = tree.ClientFile__GetBinanceHistory(strategy_idx)
            """ COMPARE """
            if (type(future_last_trade_binance) == type(file_last_trade)):
                if not future_last_trade_binance == file_last_trade:
                    """ UPDATE CLIENT FILE AND tree's HISTORY LIST """
                    tree.ClientFile__UpdateHistory(strategy_idx, future_last_trade_binance)
                else:
                    print("SAME HISTORY\n")
            else:
                """ In case the 2 transactions do not have the same type """
                return 1
    tree.ClientFile__CheckErrors()