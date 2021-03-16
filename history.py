#!/usr/bin/python3
# -*- coding: utf-8 -*-

from interface_binance import *
from constants import *

class Transaction:
    """
    A class used to represent a trade

    Attributes
    ----------
    Ìnherits all attributes from Transaction class
    
    type : str
        Type of the trade, either SPOT or FUTURES 
    
    time : int
        Timestamp of the trade

    orderId : str
        Order unique identifier of the trade
    
    symbol : str
        Currency traded

    symbol_price : float
        Price of the currency at the moment of the trade

    side : str
        Side when the trade was executed

    current_side : str
        Position side of the account after the last trade, either BUY, SELL or OUT. Set to  UNDEFINED as default value
    
    Methods
    -------
    compute_current_side(client)
        Computes the account's side (BUY/OUT).
    """
    def __init__(self, transaction_info_dict):
        self.type = UNDEFINED
        self.time = int(transaction_info_dict['time'])
        self.orderId = transaction_info_dict['orderId']
        self.symbol = transaction_info_dict['symbol']
        self.symbol_price = float(transaction_info_dict['price'])
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
    """
    A class used to represent a trade from a SPOT account, inherits from Transaction class

    Attributes
    ----------
    Ìnherits all attributes from Transaction class
    
    type : str
        Type of the trade, either SPOT or FUTURES 
    
    quantity : float
        Quantity of the currency traded

    current_side : str
        Position side of the account after the last trade, either BUY, SELL or OUT
    
    Methods
    -------
    compute_current_side(client)
        Computes the account's side (BUY/OUT).
    """
    def __init__(self, transaction_info_dict):
        super().__init__(transaction_info_dict)
        self.type = SPOT
        self.quantity = float(transaction_info_dict['origQty'])
        self.current_side = self.compute_current_side()

    def compute_current_side(self):
        """
        Name : compute_current_side(client)
    
        Parameters : client ; Client used to connect to Binance server
    
        Description : Clears the content of history_list
        """
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
    """
    A class used to represent a trade from a futures account, inherits from Transaction class

    Attributes
    ----------
    Ìnherits all attributes from Transaction class
    
    id : str
        Id of the trade
    
    realised_pnl : float
        Profit realized with the trade
    
    quantity : float
        Quantity of the currency traded

    type : str
        Type of the trade, either SPOT or FUTURES 
    
    current_side : str
        Position side of the account after the last trade, either BUY, SELL or OUT
    
    client : client.binance
        Client used to connect to Binance server

    Methods
    -------
    compute_current_side(client)
        Computes the account's side (BUY/SHORT/OUT).
    """
    def __init__(self, transaction_info_dict, client):
        super().__init__(transaction_info_dict)
        self.id = transaction_info_dict['id']
        self.realized_pnl = float(transaction_info_dict['realizedPnl'])
        self.quantity = float(transaction_info_dict['qty'])
        self.type = FUTURES
        self.current_side = self.compute_current_side(client)
        self.client = client
    
    def compute_current_side(self, client):
        """
        Name : compute_current_side(client)
    
        Parameters : client ; Client used to connect to Binance server
    
        Description : Clears the content of history_list
        """
        (positionSide, entryPrice)  = I__GET_FUTURES_POSITION(client, self.symbol)
        
        if (positionSide == SHORT):
            return SELL
        else:
            if (positionSide == BOTH) and (entryPrice != float(0)): 
                return BUY
            elif (positionSide == BOTH) and (entryPrice == float(0)):
                return OUT 
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
        List of the last Transaction made for each and every API key

    Methods
    -------
    clear()
        Clears the content of history_list

    """
    def __init__(self):
        self.history_list = []
    
    def __repr__(self):
        attributes_list = [attributes for attributes in dir(self) if not attributes.startswith('__') and not callable(getattr(self, attributes))]
        out = str()
        for attributes in attributes_list:
            out += "{0} = {1}\n".format(attributes, self.__dict__[attributes])
        return (out)
    
    def clear(self):
        """
        Name : clear()
    
        Parameters : 
    
        Description : Clears the content of history_list
        """
        self.history_list.clear()

