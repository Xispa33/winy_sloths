#!/usr/bin/python3
# -*- coding: utf-8 -*-

import bybit
from constants import *
import os
import sys
from time import *
from datetime import *
import traceback
from abc import ABC, abstractmethod
from crypto_exchange_platform import *

BUY = "Buy"
MARKET = "Market"
SELL = "Sell"
ENTRY_PRICE = "entry_price"
POSITION_VALUE = "position_value"
POSITION_MARGIN = "position_margin"

class CEP__Bybit(CryptoExchangePlatform):
    def __init__(self):
        super().__init__()
        self.name = BYBIT

    def cep__client(self, api_key, api_secret_key): 
        self.called_function_name = "cep__client"
        return (bybit.bybit(test=False, api_key=api_key, api_secret=api_secret_key))

    def cep__futures_account_trades(self, client, symbol):
        self.called_function_name = "cep__futures_account_trades"
        return client.LinearPositions.LinearPositions_myPosition(symbol=symbol).result()
    
    def cep__spot_account_trades(self, client, symbol):
        #ESSENTIAL
        self.called_function_name="cep__spot_account_trades"
        return 0


    def cep__close_long_spot(self, client, symbol):
        self.called_function_name="cep__close_long_spot"
        #ESSENTIAL
        return 0

    def cep__close_long_futures(self, client, symbol):
        self.called_function_name="cep__close_long_futures"
        bybit_positions=client.LinearPositions.LinearPositions_myPosition( \
                            symbol=symbol).result()

        if (isinstance(bybit_positions, tuple)):
            bybit_positions = bybit_positions[0][RESULT]
            for elt in bybit_positions:
                if (elt[SIZE] > 0):
                    size = elt[SIZE]
                    break
            client.LinearOrder.LinearOrder_new(side=SELL, symbol=symbol, \
                            order_type=MARKET, qty=size, \
                            time_in_force=GOODTILLCANCEL, reduce_only=True, \
                            close_on_trigger=False).result()
            return 0
        else: 
            return 1

    
    def cep__open_long_spot(self, client, symbol):
        self.called_function_name="cep__open_long_spot"
        #ESSENTIAL
        return 0

    def cep__open_long_futures(self, client, symbol, leverage, \
                                engaged_balance, entryPrice):
        self.called_function_name="cep__open_long_futures"
        client.Positions.Positions_saveLeverage(symbol=symbol, \
                                            leverage=str(leverage)).result()

        bybit_balance_response = client.Wallet.Wallet_getBalance(coin=USDT).result()
        balance=bybit_balance_response[0][RESULT][USDT][WALLET_BALANCE]
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        quantity=round(((float(balance)*engaged_balance/entryPrice) - \
                                                (5*10**(-precision - 1))), precision)
        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)

        client.LinearOrder.LinearOrder_new(side=BUY, symbol=symbol, order_type=MARKET, \
                    qty=quantity, time_in_force=GOODTILLCANCEL, reduce_only=False, \
                    close_on_trigger=False).result()

        return 0

    def cep__close_short(self, client, symbol):
        self.called_function_name="cep__close_short"

        bybit_positions=client.LinearPositions.LinearPositions_myPosition( \
                            symbol=symbol).result()

        if (isinstance(bybit_positions, tuple)):
            bybit_positions = bybit_positions[0][RESULT]
            for elt in bybit_positions:
                if (elt[SIZE] > 0):
                    size = elt[SIZE]
                    break
            client.LinearOrder.LinearOrder_new(side=BUY, symbol=symbol, \
                            order_type=MARKET, qty=size, \
                            time_in_force=GOODTILLCANCEL, reduce_only=True, \
                            close_on_trigger=False).result()
            return 0
        else: 
            return 1
    
    def cep__open_short(self, client, symbol, leverage, engaged_balance, \
                                            entryPrice):
        self.called_function_name="cep__open_short"
        
        client.Positions.Positions_saveLeverage(symbol=symbol, leverage=str(leverage)).result()

        bybit_balance_response = client.Wallet.Wallet_getBalance(coin=USDT).result()
        balance=bybit_balance_response[0][RESULT][USDT][WALLET_BALANCE]
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        quantity=round(((float(balance)*engaged_balance/entryPrice) - (5*10**(-precision - 1))), precision)
        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)

        client.LinearOrder.LinearOrder_new(side=SELL, symbol=symbol, order_type=MARKET, \
                    qty=quantity, time_in_force=GOODTILLCANCEL, reduce_only=False, \
                    close_on_trigger=False).result()

        return 0

    def cep__get_futures_account_balance(self, client):
        self.called_function_name="cep__get_futures_account_balance"
        #USELESS
        return 0


    def cep__get_asset_balance(self, client):
        self.called_function_name="cep__get_asset_balance"
        #USELESS
        return 0
    

    def cep__set_stop_loss_long(self, client, symbol, engaged_balance, \
                                entryPrice, mode, risk=RISK):
        self.called_function_name="cep__set_stop_loss_long"
        
        return 0

    def cep__set_stop_loss_short(self, client, symbol, engaged_balance, \
                                entryPrice, mode, risk=RISK):
        self.called_function_name="cep__set_stop_loss_short"
        
        return 0
    
    def cep__clear_stop_loss(self, client, symbol):
        self.called_function_name="cep__clear_stop_loss"
        return 0
    
    
    def cep__compute_side_spot_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_spot_account"
        # ESSENTIAL
        if (not isinstance(cep_response, tuple)):
            #print("Bybit return was crap ! \n")
            return account.side
        else:
            bybit_response = cep_response[0][RESULT]
            return account.side
        
    
    def cep__compute_side_futures_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_futures_account"
        if (not isinstance(cep_response, tuple)):
            #print("Bybit return was crap ! \n")
            return account.side
        else:
            bybit_response = cep_response[0][RESULT]
            if (not isinstance(bybit_response, list)):
                return account.side
            else:
                for elt in bybit_response:
                    if (elt[SIZE] > 0):
                        account.markPrice = 0
                        account.entryPrice = round(float(elt[ENTRY_PRICE]), 0)
                        account.leverage = elt[LEVERAGE]
                        # UNDERSTAND DIFFERENCE BETWEEN positionAmt AND engaged_balance
                        account.positionAmt = 0
                        account.engaged_balance = float(elt[POSITION_VALUE])
                        account.balance = float(elt[POSITION_MARGIN])
                        if (elt[SIDE]) == BUY:
                            return LONG 
                        elif (elt[SIDE]) == SELL:
                            return SHORT
                return account.side

    
    def cep__compute_engaged_balance(self, account, cep_response):
        self.called_function_name="cep__compute_engaged_balance"
        #USELESS
        return 0
        
    
