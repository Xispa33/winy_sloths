#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from binance.client import Client
from interface_binance import *

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

    def ClientFile__ReadHistory(self):
        self.history.clear()
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

    def ClientFile__WriteHistory(self):
        self.history.clear()
        with open(self.client_file_path, 'rw') as txt_file:
            info = txt_file.readlines()    
            #read history
            for i in range(0,self.header.all_strategies_nb):
                strategy_history = info[2+self.header.all_strategies_nb+i+1].rstrip('\n').split(';')
                last_transaction = Transaction(strategy_history)
                print(last_transaction)
                self.history.history_list.append(last_transaction)
                #print(strategy_history)
                    
            txt_file.close()
    
    def is_strategy_idx_valid(self, strategy_idx):
        for key in self.header.key_list:
            if key.strategie_idx == strategy_idx:
                return True
        return False

    def find_strategy_api_key(self, strategy_idx):
        if (self.is_strategy_idx_valid(strategy_idx)):
            for key in self.header.key_list:
                if key.strategie_idx == strategy_idx:
                    return (key.header.api_key, key.header.api_secret_key)
        else:
            return 1

    def get_last_futures_trade(self, strategy_idx):
        credentials = self.find_strategy_api_key(strategy_idx)
        client = Client(credentials[0], credentials[1])
        trades_list = I__FUTURES_ACCOUNT_TRADES(client)
        
        if (trades_list != 1):
            return trades_list[-1]
        else:
            return 2

    def ClientFile__GetLastTrade(self):


if __name__ == "__main__":
    tree = ClientFile("history.txt")
    print(tree)

    while (1):
