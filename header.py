#!/usr/bin/python3
# -*- coding: utf-8 -*-

from binance.client import Client
from interface_binance import *

class Header:
    """
    A class used to represent the header of a client file

    Attributes
    ----------
    client_name : str
        A formatted string with the client's name
    nb_keys : int
        Number of API keys provided by the client
    all_strategies_nb : int
        Maximum number of strategies a client can register to
    key_list : list
        List of all the keys provided by the client

    Methods
    -------
    
    """
    def __init__(self):
        self.client_name = str()
        self.nb_keys = 0
        self.all_strategies_nb = 6
        self.key_list = []
        self.cpt_strategies = 0
    
    def __repr__(self):
        attributes_list = [attributes for attributes in dir(self) if not attributes.startswith('__') and not callable(getattr(self, attributes))]
        out = str()
        for attributes in attributes_list:
            out += "{0} = {1}\n".format(attributes, self.__dict__[attributes])
        return (out)
    
    def check_header(self):
        out_message = " {} header file is ".format(self.client_name)
        
        if (self.nb_keys <=  0):
            out_message += "incorrect ! \nReason: Number of keys = {}. Should be stricly superior 0.\n".format(self.nb_keys)
            return 1
        elif (self.cpt_strategies != self.nb_keys):
            out_message += "incorrect ! \nReason: Number of strategies = {}. Should be equal to the number of keys ({}).\n".format(self.cpt_strategies, self.nb_keys)
            return 2
        elif (self.all_strategies_nb < self.cpt_strategies):
            out_message += "incorrect ! \nReason: Number of strategies = {}.Should be inferior or equal to {} o equal or less than 0.\n".format(self.cpt_strategies, self.all_strategies_nbs)
            return 3
        elif (self.all_strategies_nb < self.nb_keys):
            out_message += "incorrect ! \nReason: Number of keys = {}. Should be inferior or equal to {} o equal or less than 0.\n".format(self.nb_keys, self.all_strategies_nb)
            return 4
        else:
            out_message += "correct !\n"
            return 0  

    def check_keys_list(self):
        ret = 1
        err_flag = 0
        for key in self.key_list:
            ret = key.check_key()
            if ret != 0:
                print("Strategy index {} credentials for {} are invalid ! \n".format(key.strategy_idx, self.client_name))
                err_flag = 1
        
        return err_flag

class ApiKeyClass:
    """
    A class used to gather all relevant information of an API key

    Attributes
    ----------
    strategy_idx : int
        Strategy index associated with the API key

    api_key : str
        A formatted string with the API key
    
    api_secret_key : int
        A formatted string with the API key secret code 
    
    api_validity : int
        For indicating the validity of the API key pair. If the pair allowed to access binance, the flag is equal to 0, else 1
    
    account_type : str
        A formatted string, either SPOT/FUTURE indicating the type of account

    Methods
    -------
    
    """
    def __init__(self, strategy_idx, api_key, api_secret_key, api_validity, account_type):
        self.strategy_idx = strategy_idx
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.api_validity = api_validity
        self.account_type = account_type

    def __repr__(self):
        out = str()
        out += "\n**********************\n"
        out += "STRATEGY NUMBER : {}\n".format(self.strategy_idx)
        out += "API KEY : {}\n".format(self.api_key)
        out += "API KEY SECRET : {}\n".format(self.api_secret_key)
        out += "API KEY VALIDITY FLAG : {}\n".format(self.api_validity)
        out += "API KEY ACCOUNT TYPE : {}\n".format(self.account_type)
        out += "**********************\n"
        return out
    
    def check_key(self):
        
        client = Client(self.api_key, self.api_secret_key)
        
        self.api_validity = I__GET_SYSTEM_STATUS(client)

        return self.api_validity