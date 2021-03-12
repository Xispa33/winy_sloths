#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
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
        #print(attributes_list)
        out = str()
        for attributes in attributes_list:
            out += "{0} = {1}\n".format(attributes, self.__dict__[attributes]) if attributes != attributes_list[-1] else "{0} = {1}".format(attributes, self.__dict__[attributes])
        return (out)

class History:
    """
    A class used to represent the history of a client file

    Attributes
    ----------
    history : list
        List of the last 5 trades made for each and every API key

    Methods
    -------
    
    """
    def __init__(self):
        self.history_list = []
    
    def __repr__(self):
        attributes_list = [attributes for attributes in dir(self) if not attributes.startswith('__') and not callable(getattr(self, attributes))]
        out = str()
        for attributes in attributes_list:
            out += "{0} = {1}\n".format(attributes, self.__dict__[attributes]) if attributes != attributes_list[-1] else "{0} = {1}".format(attributes, self.__dict__[attributes])
        return (out)

class ApiKeyClass:
    """
    A class used to gather all relevant information of an API key

    Attributes
    ----------
    strategie_idx : int
        Strategy index associated with the API key

    api_key : str
        A formatted string with the API key
    
    api_secret_key : int
        A formatted string with the API key secret code 
    
    api_validity : int
        For indicating the validity of the API key pair. If the pair allowed to access binance, the flag is equal to 0, else 1
    Methods
    -------
    
    """
    def __init__(self, strategie_idx, api_key, api_secret_key, api_validity):
        self.strategie_idx = strategie_idx
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.api_validity = api_validity

    def __repr__(self):
        out = str()
        out += "STRATEGY NUMBER : {}\n".format(self.strategie_idx)
        out += "API KEY : {}\n".format(self.api_key)
        out += "API KEY SECRET : {}\n".format(self.api_secret_key)
        out += "API KEY VALIDITY FLAG : {}".format(self.api_validity)
        return out

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
        self.return_tuple     = (1,1,1,1) #(read_file_return, check_file_header_return, check_file_keys_return, check_file_history_return)
        self.init_status      = self.ClientFile__Init()
        
        if (self.init_status != 0):
            print("KO")
            #send_mail
        else:
            print("OK")

    """
    def __repr__(self):
        attributes_list = [attributes for attributes in dir(self) if not attributes.startswith('__') and not callable(getattr(self, attributes))]
        #print(attributes_list)
        out = str()
        for attributes in attributes_list:
            out += "{0} = {1}\n".format(attributes, self.__dict__[attributes]) if attributes != attributes_list[-1] else "{0} = {1}".format(attributes, self.__dict__[attributes])
        return (out)
    """
    def read_file(self):
        cpt_strategies = 0
        try:
            with open(self.client_file_path, 'r') as txt_file:
                info = txt_file.readlines()
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
                    
                txt_file.close()
                    
            return 0
                
        except:
            return 1 

    def check_header_info(self):
        #liste de verif:
            #verifier que fichier existe
            #verifier que client existe ?
            #verifier que liste des cles est non vide
            #verifier que nb_key > 0 et < nb_strategies
            #verifier que toutes les paires de cles permettent de se connecter à Binance
            # Ajouter : clé unique
        out_message = " {} header file is ".format(self.header.client_name)
        
        if (self.header.nb_keys <=  0):
            out_message += "incorrect ! \nReason: Number of keys = {}. Should be stricly superior 0.\n".format(self.header.nb_keys)
            return 1
        elif (self.header.cpt_strategies != self.header.nb_keys):
            out_message += "incorrect ! \nReason: Number of strategies = {}. Should be equal to the number of keys ({}).\n".format(self.header.cpt_strategies, self.header.nb_keys)
            return 2
        elif (self.header.all_strategies_nb < self.header.cpt_strategies):
            out_message += "incorrect ! \nReason: Number of strategies = {}.Should be inferior or equal to {} o equal or less than 0.\n".format(self.header.cpt_strategies, self.header.all_strategies_nbs)
            return 3
        elif (self.header.all_strategies_nb < self.header.nb_keys):
            out_message += "incorrect ! \nReason: Number of keys = {}. Should be inferior or equal to {} o equal or less than 0.\n".format(self.header.nb_keys, self.header.all_strategies_nb)
            return 3
        #python file does not exist
        elif (0):
            out_message += "incorrect ! \nReason: File {} does not exist.\n".format(self.client_file_path)
            #elif self.header.client_file_path
        else:
            out_message += "correct !\n"
            return 0  

    def check_header_keys(self):
        validity_out = []
        ping_ret = 1
        for api_keys in self.header.key_list:
            #print(api_keys[0][0])
            client = Client(api_keys.api_key, api_keys.api_secret_key)
            ping_ret = I__GET_SYSTEM_STATUS(client)
            api_keys.api_validity = ping_ret
            validity_out.append(ping_ret)
        
        # TODO: Ajouter message pour dire quelles clés sont incorrectes
        for value in validity_out:
            if (value != 0):
                return 1
        
        return 0
            
    
    def check_history(self):
        print("tata")
        return 0

    """
    1 - Lecture du fichier client
    2 - Si pas d'erreur, verification de l'intégrité des données ; Si erreur, on sort
    3 - Verification du header - Si header OK, on passe à la suite, sinon on arrete
    4 - Verification de l'historique - Si historique OK, on passe à la suite, sinon on arrete
    """
        
    def ClientFile__Init(self):
        #(read_file_return, check_file_header_return, check_file_keys_return, check_file_history_return)
        self.return_tuple = (self.read_file(), self.check_header_info(), self.check_header_keys(),self.check_history())
        if ( (self.return_tuple[0] != 0) or (self.return_tuple[1] != 0) or (self.return_tuple[2] != 0) or (self.return_tuple[3] != 0)):
            #send mail 
            #TODO ici, si jamais une clé est mauvaise, il faut envoyer un mail avec le nombre de clé mauvaises et les stratégies correspondantes
            print("KO")
            print(self.return_tuple)
            return 1
        else:
            print("OK")
            return 0

    
a = ClientFile("history.txt")
#a.read_client_file()
print(a)