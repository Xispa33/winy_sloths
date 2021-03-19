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
    
    convert_raw_trade_to_transaction(raw_trade, client)
        Converts the dictionnary returned by Binance into a Transaction object 
    """
    def __init__(self, transaction_info_dict):
        self.type = UNDEFINED
        self.time = int(transaction_info_dict[TIME])
        self.orderId = transaction_info_dict[ORDER_ID]
        self.symbol = transaction_info_dict[SYMBOL]
        self.symbol_price = float(transaction_info_dict[PRICE])
        self.side = transaction_info_dict[SIDE]
        self.current_side = UNDEFINED

    def compute_current_side(self):
        """
        Name : compute_current_side()
    
        Parameters : 
    
        Description : Computes the current position of an account (FUTURE or SPOT).
        """
        return 0

    def __repr__(self):
        attributes_list = [attributes for attributes in dir(self) if not attributes.startswith('__') and not callable(getattr(self, attributes))]
        out = str()
        for attributes in attributes_list:
            out += "{0} = {1}\n".format(attributes, self.__dict__[attributes])
        return (out)
    
    def __eq__(self,other_history):
        return ((self.orderId == other_history.orderId) and (self.symbol == other_history.symbol) and (self.symbol_price == other_history.symbol_price) and (self.side == other_history.side))

    @staticmethod
    def convert_raw_trade_to_transaction(raw_trade, client):
        """
        Name : convert_raw_trade_to_transaction(raw_trade, client)
    
        Parameters : 
    
        Description : Converts the dictionnary returned by Binance into a Transaction object (either FUTURES or SPOT)
        """
        if isinstance(raw_trade, dict):
            if REALIZED_PNL in raw_trade:
                """ Futures transaction """
                return TransactionFutures.convert_to_futures(raw_trade, client)
            else:
                """ Spot transaction """
                return TransactionSpot.convert_to_spot(raw_trade)
        else:
            return 1
    
    @staticmethod
    def create_transaction(account_type, strategy_history, client):
        if (account_type == FUTURES):
            dict_keys_list = [TYPE, TIME, ID, ORDER_ID, SYMBOL, PRICE, SIDE, QTY, REALIZED_PNL, CURRENT_SIDE]
            strategy_history_dict = {dict_keys_list[i]:strategy_history[i] for i in range(0, len(dict_keys_list))}
            return (TransactionFutures(strategy_history_dict, client)) 
        elif (account_type == SPOT):
            dict_keys_list = [TYPE, TIME, ORDER_ID, SYMBOL, PRICE, SIDE, ORIGQTY, CURRENT_SIDE]
            strategy_history_dict = {dict_keys_list[i]:strategy_history[i] for i in range(0, len(dict_keys_list))}
            return (TransactionSpot(strategy_history_dict))
        else:
            return 1

class TransactionSpot(Transaction):
    """
    A class used to represent a trade from a SPOT account, inherits from Transaction class
    In the client file, Futures transactions are organized as follow:

    time | id | orderId | symbol | symbol_price | side | quantity | current_side

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

    convert_to_spot(raw_trade)
        Converts the dictionnary returned by Binance into a TransactionSpot object. Below is an example of a 
        dictionnary that could be returned by Binace for a SPOT account:
        {'symbol': 'BTCUSDT', 'orderId': 5211308012, 'orderListId': -1, 'clientOrderId': 'x-K309V22B-km7ojj23ybr0kzjtq6m', 'price': '59800.76000000', 'origQty': '0.02100000', 'executedQty': '0.02100000', 'cummulativeQuoteQty': '1255.81596000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1615636978951, 'updateTime': 1615637009689, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}
    """
    def __init__(self, transaction_info_dict):
        super().__init__(transaction_info_dict)
        self.type = SPOT
        self.quantity = float(transaction_info_dict[ORIGQTY])
        self.current_side = self.compute_current_side()

    def compute_current_side(self):
        """
        Name : compute_current_side()
    
        Parameters : 
    
        Description : Computes the current position of an account (FUTURE or SPOT).
        """
        if self.side == BUY: 
            return BUY
        elif self.side == SELL:
            return OUT
        else:
            return 1
    
    def __str__(self):
        out = "{};{};{};{};{};{};{};{}\n".format(str(self.type), str(self.time), str(self.orderId), str(self.symbol), \
            str(self.symbol_price), str(self.side), str(self.quantity), str(self.current_side))
        return out

    @staticmethod
    def convert_to_spot(raw_trade):
        """
        Name : convert_to_spot(raw_trade)
    
        Parameters : raw_trade; raw dictionnary returned by Binance
    
        Description : Converts the dictionnary returned by Binance into a TransactionSpot object. Below is an example of a 
                      dictionnary that could be returned by Binace for a SPOT account:
                      {'symbol': 'BTCUSDT', 'orderId': 5211308012, 'orderListId': -1, 'clientOrderId': 'x-K309V22B-km7ojj23ybr0kzjtq6m', 'price': '59800.76000000', 'origQty': '0.02100000', 'executedQty': '0.02100000', 'cummulativeQuoteQty': '1255.81596000', 'status': 'FILLED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'BUY', 'stopPrice': '0.00000000', 'icebergQty': '0.00000000', 'time': 1615636978951, 'updateTime': 1615637009689, 'isWorking': True, 'origQuoteOrderQty': '0.00000000'}
        """
        return TransactionSpot(raw_trade)

class TransactionFutures(Transaction):
    """
    A class used to represent a trade from a futures account, inherits from Transaction class
    In the client file, Futures transactions are organized as follow:

    time | id | orderId | symbol | symbol_price | side | quantity | realized_pnl | current_side

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
    
    convert_to_futures(raw_trade, client)
        Converts the dictionnary returned by Binance into a TransactionFutures object. Below is an example of a 
        dictionnary that could be returned by Binace for a FUTURES account:
        {'symbol': 'ETHUSDT', 'id': 384187499, 'orderId': 8389765493651748878, 'side': 'SELL', 'price': '1535.45', 'qty': '1.474', 'realizedPnl': '0', 'marginAsset': 'USDT', 'quoteQty': '2263.25330', 'commission': '0.45265066', 'commissionAsset': 'USDT', 'time': 1614974810111, 'positionSide': 'BOTH', 'maker': True, 'buyer': False}
    """
    def __init__(self, transaction_info_dict, client):
        super().__init__(transaction_info_dict)
        self.id = transaction_info_dict[ID]
        self.realized_pnl = float(transaction_info_dict[REALIZED_PNL])
        self.quantity = float(transaction_info_dict[QTY])
        self.type = FUTURES
        self.current_side = self.compute_current_side(client)
        self.client = client
    
    def compute_current_side(self, client):
        """
        Name : compute_current_side()
    
        Parameters : client ; Client used to connect to Binance server
    
        Description : Computes the current position of an account (FUTURE or SPOT).
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
        out = "{};{};{};{};{};{};{};{};{};{}\n".format(str(self.type), str(self.time), str(self.id), str(self.orderId), str(self.symbol), \
            str(self.symbol_price), str(self.side), str(self.quantity), str(self.realized_pnl), str(self.current_side))
        return out

    @staticmethod
    def convert_to_futures(raw_trade, client):
        """
        Name : convert_to_futures(raw_trade, client)
    
        Parameters : client ; Client used to connect to Binance server
                     raw_trade; raw dictionnary returned by Binance
    
        Description : Converts the dictionnary returned by Binance into a TransactionFutures object. Below is an example of a 
                      dictionnary that could be returned by Binace for a FUTURES account:
                      {'symbol': 'ETHUSDT', 'id': 384187499, 'orderId': 8389765493651748878, 'side': 'SELL', 'price': '1535.45', 'qty': '1.474', 'realizedPnl': '0', 'marginAsset': 'USDT', 'quoteQty': '2263.25330', 'commission': '0.45265066', 'commissionAsset': 'USDT', 'time': 1614974810111, 'positionSide': 'BOTH', 'maker': True, 'buyer': False}
        """
        
        return TransactionFutures(raw_trade, client)

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
    
    add_transaction(transaction)
        Adds a Transaction object in history_list
    """
    def __init__(self):
        self.history_list = []
    
    def __repr__(self):
        attributes_list = [attributes for attributes in dir(self) if not attributes.startswith('__') and not callable(getattr(self, attributes))]
        out = str()
        for attributes in attributes_list:
            out += "{0} = {1}\n".format(attributes, self.__dict__[attributes])
        return (out)
    
    def __getattr__(self, idx):
        return self.history_list[idx]
    
    def add_transaction(self, transaction):
        """
        Name : add_transaction()
    
        Parameters : transaction ; Transaction object added in history_list
    
        Description : Adds a Transaction object in history_list
        """
        self.history_list.append(transaction) 
    
    def clear(self):
        """
        Name : clear()
    
        Parameters : 
    
        Description : Clears the content of history_list
        """
        self.history_list.clear()

