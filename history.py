#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Transaction:
    #def __init__(self, time, id, orderId, symbol, symbol_price, initial_side, side, new_side, quantity, realized_pnl):
    def __init__(self, transaction_info_list):
        self.time = transaction_info_list[0]
        self.id = transaction_info_list[1]
        self.orderId = transaction_info_list[2]
        self.symbol = transaction_info_list[3]
        self.symbol_price = transaction_info_list[4]
        self.initial_side = "NEUTRE"
        self.side = transaction_info_list[5]
        self.quantity = transaction_info_list[6]
        self.realized_pnl = transaction_info_list[7]
        self.new_side = self.compute_new_side()

    def compute_new_side(self):
        self.new_side = "NEUTRE"

    def __repr__(self):
        attributes_list = [attributes for attributes in dir(self) if not attributes.startswith('__') and not callable(getattr(self, attributes))]
        out = str()
        for attributes in attributes_list:
            out += "{0} = {1}\n".format(attributes, self.__dict__[attributes])
        return (out)

    def __eq__(self,other_history):
        return ((self.orderId == other_history.orderId) and (self.symbol == other_history.symbol) and (self.symbol_price == other_history.symbol_price) and (self.side == other_history.side))

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
        self.max_nb_transaction = 10
        self.strategy_idx = 0
    
    def __repr__(self):
        attributes_list = [attributes for attributes in dir(self) if not attributes.startswith('__') and not callable(getattr(self, attributes))]
        out = str()
        for attributes in attributes_list:
            out += "{0} = {1}\n".format(attributes, self.__dict__[attributes])
        return (out)
    
    def clear(self):
        self.history_list.clear()

    def check_history(self):
        print("tata")
        return 0

