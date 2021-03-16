#!/usr/bin/python3
# -*- coding: utf-8 -*-

from interface_binance import *
from constants import *

class Transaction:
    #def __init__(self, time, id, orderId, symbol, symbol_price, initial_side, side, new_side, quantity, realized_pnl):
    def __init__(self, transaction_info_dict):
        self.type = UNDEFINED
        self.time = transaction_info_dict['time']
        #self.id = transaction_info_list[1]
        self.orderId = transaction_info_dict['orderId']
        self.symbol = transaction_info_dict['symbol']
        self.symbol_price = transaction_info_dict['price']
        self.side = transaction_info_dict['side']
        self.current_side = UNDEFINED

    def compute_current_side(self):
        return 0

    def __repr__(self):
        attributes_list = [attributes for attributes in dir(self) if not attributes.startswith('__') and not callable(getattr(self, attributes))]
        out = str()
        for attributes in attributes_list:
            out += "{0} = {1}\n".format(attributes, self.__dict__[attributes])
        return (out)
    
    def __eq__(self,other_history):
        return ((self.orderId == other_history.orderId) and (self.symbol == other_history.symbol) and (self.symbol_price == other_history.symbol_price) and (self.side == other_history.side))

class TransactionSpot(Transaction):
    def __init__(self, transaction_info_dict):
        super().__init__(transaction_info_dict)
        self.type = SPOT
        self.quantity = transaction_info_dict['origQty']
        self.current_side = self.compute_current_side()

    def compute_current_side(self):
        if self.side == BUY: 
            return BUY
        elif self.side == SELL:
            return OUT
        else:
            return 1
    
    def __str__(self):
        # time | id | orderId | symbol | symbol_price | side | quantity | current_side
        out = "{};{};{};{};{};{};{};{}\n".format(str(self.type), str(self.time), str(self.orderId), str(self.symbol), \
            str(self.symbol_price), str(self.side), str(self.quantity), str(self.current_side))
        return out

class TransactionFutures(Transaction):
    def __init__(self, transaction_info_dict, client):
        super().__init__(transaction_info_dict)
        self.id = transaction_info_dict['id']
        self.realized_pnl = transaction_info_dict['realizedPnl']
        self.quantity = transaction_info_dict['qty']
        self.type = FUTURES
        self.current_side = self.compute_current_side(client)
        self.client = client
    
    def compute_current_side(self, client):
        (positionSide, entryPrice)  = I__GET_FUTURES_POSITION(client, self.symbol)
        
        if (positionSide == BOTH) and (entryPrice != float(0)): 
            return BUY
        elif (positionSide == BOTH) and (entryPrice == float(0)):
            return OUT
        elif positionSide == SHORT:
            return SELL
        else:
            return 1

    def __str__(self):
        # time | id | orderId | symbol | symbol_price | side | quantity | realized_pnl | current_side
        out = "{};{};{};{};{};{};{};{};{};{}\n".format(str(self.type), str(self.time), str(self.id), str(self.orderId), str(self.symbol), \
            str(self.symbol_price), str(self.side), str(self.quantity), str(self.realized_pnl), str(self.current_side))
        return out

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

