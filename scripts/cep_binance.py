#!/usr/bin/python3
# -*- coding: utf-8 -*-

from binance.client import Client
import binance
from constants import *
import os
import sys
from time import *
from datetime import *
import traceback
from abc import ABC, abstractmethod
from crypto_exchange_platform import *

class CEP__Binance(CryptoExchangePlatform):
    """
    Description :
        This class represents a Binance object. It contains all basic functions
        enabling trading on Binance.
    Attributes
    ----------
    name : str
        Name of the cryptocurrency exchange platform. Here Binance
    
    Methods
    -------
    cep__client()
    cep__futures_account_trades()
    cep__spot_account_trades()
    cep__close_long_spot()
    cep__close_long_futures()
    cep__open_long_futures()
    cep__open_long_spot()
    cep__close_short()
    cep__open_short()
    cep__get_futures_account_balance()
    cep__get_asset_balance()
    cep__set_stop_loss_long
    cep__set_stop_loss_short()
    cep__clear_stop_loss()
    cep__compute_side_spot_account()
    cep__compute_side_futures_account()
    cep__compute_engaged_balance()
    """
    def __init__(self):
        super().__init__()
        self.name = BINANCE

    def cep__client(self, api_key, api_secret_key, account_contract_type): 
        self.called_function_name = "cep__client"
        return (Client(api_key, api_secret_key))

    def cep__futures_account_trades(self, client, symbol):
        self.called_function_name = "cep__futures_account_trades"
        return client.futures_position_information(symbol=symbol, \
                      timestamp=client.futures_time())
    
    def cep__spot_account_trades(self, client, symbol):
        self.called_function_name="cep__spot_account_trades"
        return (client.get_all_orders(symbol=symbol, limit='1'))


    def cep__close_long_spot(self, client, symbol):
        self.called_function_name="cep__close_long_spot"
        curr_asset = self.ALL_SYMBOLS_DICT[symbol][ASSET_IDX]
        price = client.get_avg_price(symbol=symbol)[PRICE]
        asset = round(float(client.get_asset_balance( \
                        asset=curr_asset)[FREE])*float(price) - 1,1)
        client.create_order(symbol=symbol, side=SELL, type=MARKET, \
                            quoteOrderQty=abs(asset), \
                            timestamp=client.get_server_time())
        return 0

    def cep__close_long_futures(self, client, symbol):
        self.called_function_name="cep__close_long_futures"
        last_trade = []
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]

        if last_trade == []:
            last_trade = self.CEP__FUTURES_ACCOUNT_TRADES(client, symbol)
        else:
            pass
        
        for dic in last_trade:
            if dic[POSITION_SIDE] == LONG:
                ret = dic
        
        position_amt = round(float(ret[POSITION_AMT]), precision)
        if (position_amt != 0.0):
            client.futures_create_order(symbol=symbol, positionside=LONG, \
                                        side=SELL, type=MARKET, \
                                        quantity=position_amt, \
                                        timestamp=client.futures_time())
        else:
            pass
        
        return 0

    
    def cep__open_long_spot(self, client, symbol):
        self.called_function_name="cep__open_long_spot"

        usdt_asset = client.get_asset_balance(asset=USDT)[FREE]
        asset_round=round(float(usdt_asset)-0.05,1)
        client.create_order(symbol=symbol, side=BUY, type=MARKET, \
                            quoteOrderQty=asset_round, \
                            timestamp=client.get_server_time())
        return 0

    def cep__open_long_futures(self, client, symbol, leverage, \
                                engaged_balance, entryPrice):
        self.called_function_name="cep__open_long_futures"

        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]
        ret = client.futures_position_information(symbol=symbol, \
                                                  timestamp=client.futures_time())
        if (len(ret) == 1):
            client.futures_change_position_mode(dualSidePosition=TRUE, \
                                                timestamp=client.futures_time())
        
        client.futures_change_leverage(symbol=symbol, leverage=leverage, \
                                       timestamp=client.futures_time())
        
        bin_ret=client.futures_account_balance(timestamp=client.futures_time())

        for dic in bin_ret:
            if dic[ASSET] == USDT:
                ret = dic

        balance=ret[WITHDRAW_AVAILABLE]

        quantity=round(((float(balance)*engaged_balance/entryPrice) - \
                                                    (5*10**(-precision-1))),precision)

        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)
        
        client.futures_create_order(symbol=symbol, side=BUY, positionSide=LONG, \
                                    type=MARKET, quantity=quantity, \
                                    timestamp=client.futures_time())
        
        return 0

    def cep__close_short(self, client, symbol):
        self.called_function_name="cep__close_short"
        last_trade = []
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]

        if last_trade == []:
            last_trade = self.CEP__FUTURES_ACCOUNT_TRADES(client, symbol)
        else:
            pass
            
        for dic in last_trade:
            if dic[POSITION_SIDE] == SHORT:
                ret = dic
        
        quantity = round(abs(float(ret[POSITION_AMT])), precision)

        if (quantity != 0.0):
            client.futures_create_order(symbol=symbol, positionside=SHORT, \
                                        side=BUY, type=MARKET, quantity=quantity, \
                                        timestamp=client.futures_time())
        else:
            pass
            
        return 0
    
    def cep__open_short(self, client, symbol, leverage, engaged_balance, \
                                            entryPrice):
        self.called_function_name="cep__open_short"
        precision = self.ALL_SYMBOLS_DICT[symbol][PRECISION_IDX]

        ret = client.futures_position_information(symbol=symbol, \
                                                  timestamp=client.futures_time())
        if (len(ret) == 1):
            client.futures_change_position_mode(dualSidePosition=TRUE, \
                                                timestamp=client.futures_time())
        
        client.futures_change_leverage(symbol=symbol, leverage=leverage, \
                                       timestamp=client.futures_time())

        bin_ret=client.futures_account_balance(timestamp=client.futures_time())
        
        for dic in bin_ret:
            if dic[ASSET] == USDT:
                ret = dic
        
        balance=ret[WITHDRAW_AVAILABLE]

        quantity = round(((float(balance)*abs(engaged_balance)/entryPrice) - \
                                                    (5*10**(-precision - 1))), precision)

        if (quantity < (1*10**(-precision))):
            quantity = 1*10**(-precision)
        
        client.futures_create_order(symbol=symbol, side=SELL, positionSide=SHORT, \
                                    type=MARKET, quantity=quantity, \
                                    timestamp=client.futures_time())
            
        return 0

    def cep__get_futures_account_balance(self, client):
        self.called_function_name="cep__get_futures_account_balance"
        ret = 1
        bin_ret = client.futures_account_balance(timestamp=client.futures_time())
        for dic in bin_ret:
            if dic[ASSET] == USDT:
                ret = dic
        return ret 


    def cep__get_asset_balance(self, client):
        self.called_function_name="cep__get_asset_balance"
        return client.get_asset_balance(asset=USDT)
    

    def cep__set_stop_loss_long(self, client, symbol, engaged_balance, \
                                entryPrice, mode, risk=RISK):
        self.called_function_name="cep__set_stop_loss_long"
        ret = 0
        price=(1 - (risk/engaged_balance))*entryPrice
        if (mode == HEDGE):
            client.futures_create_order(symbol=symbol, side=SELL, \
                                        positionSide=LONG, closeposition=TRUE, \
                                        stopPrice=round(float(price),0), \
                                        type=STOP_MARKET, \
                                        timestamp=client.futures_time())
        elif (mode == ONE_WAY):
            client.futures_create_order(symbol=symbol, side=SELL, \
                                        closeposition=TRUE, \
                                        stopPrice=round(float(price),0), \
                                        type=STOP_MARKET, \
                                        timestamp=client.futures_time())
        else:
            ret = 1
        
        return ret

    def cep__set_stop_loss_short(self, client, symbol, engaged_balance, \
                                entryPrice, mode, risk=RISK):
        self.called_function_name="cep__set_stop_loss_short"
        ret = 0
        price=(1 + (RISK/engaged_balance))*entryPrice
        if (mode == HEDGE):
            client.futures_create_order(symbol=symbol, side=BUY, positionSide=SHORT, \
                                        closeposition=TRUE, stopPrice=round(float(price),0), \
                                        type=STOP_MARKET, \
                                        timestamp=client.futures_time())
        elif (mode == ONE_WAY):
            client.futures_create_order(symbol=symbol, side=BUY, closeposition=TRUE, \
                                        stopPrice=round(float(price),0), type=STOP_MARKET, \
                                        timestamp=client.futures_time())
        else:
            ret = 1
        
        return ret
    
    def cep__clear_stop_loss(self, client, symbol):
        self.called_function_name="cep__clear_stop_loss"
        return client.futures_cancel_all_open_orders(symbol=symbol, countdownTime=0, \
                                                     timestamp=client.futures_time())
    
    
    def cep__compute_side_spot_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_spot_account"

        if (isinstance(cep_response, int)):
            #print("Binance return was crap ! \n")
            return account.side
        else:
            if (len(cep_response) == 0):
                return account.side
            else:
                asset_dict = self.CEP__GET_ASSET_BALANCE( \
                                self.CEP__CLIENT(account.api_key._api_key, \
                                account.api_key._api_secret_key, None))
            
                if (not isinstance(asset_dict, dict)):
                    return account.side
                else:
                    binance_response = cep_response[0]
                    asset_usdt=float(asset_dict[FREE])

                    if binance_response[SIDE] == BUY and \
                       round(float(asset_usdt),1) < MIN_WALLET_IN_USDT: 
                        return LONG
                    elif binance_response[SIDE] == SELL and \
                         round(float(asset_usdt),1) > MIN_WALLET_IN_USDT:
                        return OUT
                    else:
                        return account.side
    
    def cep__compute_side_futures_account(self, account, cep_response):
        self.called_function_name="cep__compute_side_futures_account"
        if (isinstance(cep_response, int)):
            #print("Binance return was crap ! \n")
            return account.side
        else:
            binance_response = cep_response
            if (len(binance_response) > 1):
                account.account_mode = HEDGE
                for dic in binance_response:
                    if dic[POSITION_SIDE] == BOTH:
                        both_list = dic
                    elif dic[POSITION_SIDE] == LONG:
                        long_list = dic
                    else:
                        short_list = dic
                
                entry_price_both = float(both_list[ENTRY_PRICE])
                entry_price_long = float(long_list[ENTRY_PRICE])
                entry_price_short = float(short_list[ENTRY_PRICE])

                if (entry_price_both != float(0)) or (entry_price_long != float(0)):
                    account.markPrice = round(float(long_list[MARK_PRICE]), 0)
                    account.entryPrice = round(float(long_list[ENTRY_PRICE]), 0)
                    account.leverage = long_list[LEVERAGE]
                    account.positionAmt = float(long_list[POSITION_AMT])
                    account.balance = float(self.CEP__GET_FUTURES_ACCOUNT_BALANCE( \
                                            self.CEP__CLIENT(account.api_key._api_key, \
                                            account.api_key._api_secret_key, None))[BALANCE])
                    ret = self.cep__compute_engaged_balance(account, binance_response)
                    if ret == 1:
                        return OUT
                    else:
                        return LONG
                elif (entry_price_both == float(0) and \
                      entry_price_long == float(0) and \
                      entry_price_short == float(0)):
                    return OUT
                elif (entry_price_short != float(0)):
                    account.markPrice = round(float(short_list[MARK_PRICE]), 0)
                    account.entryPrice = round(float(short_list[ENTRY_PRICE]), 0)
                    account.leverage = short_list[LEVERAGE]
                    account.positionAmt = float(short_list[POSITION_AMT])
                    account.balance = float(self.CEP__GET_FUTURES_ACCOUNT_BALANCE( \
                                            self.CEP__CLIENT(account.api_key._api_key, \
                                            account.api_key._api_secret_key, None))[BALANCE])
                    ret = self.cep__compute_engaged_balance(account, binance_response)
                    if ret == 1:
                        return OUT
                    else:
                        return SHORT
                else:
                    return account.side
            else:
                # Store needed information for FUTURES account
                account.account_mode = ONE_WAY
                account.markPrice = round(float(binance_response[0][MARK_PRICE]), 0)
                account.entryPrice = round(float(binance_response[0][ENTRY_PRICE]), 0)
                account.leverage = binance_response[0][LEVERAGE]
                account.positionAmt = float(binance_response[0][POSITION_AMT])
                
                bin_ret = self.CEP__GET_FUTURES_ACCOUNT_BALANCE( \
                                self.CEP__CLIENT(account.api_key._api_key, \
                                                 account.api_key._api_secret_key, None))
                if (isinstance(bin_ret, int)):
                    return account.side
                else:
                    account.balance = float(bin_ret[BALANCE])
                
                ret = self.cep__compute_engaged_balance(account, binance_response)
                
                if (account.positionAmt == float(0) or ret == 1):
                    return OUT
                elif (account.positionAmt < 0):
                    return SHORT
                elif (account.positionAmt > 0):
                    return LONG
                else: 
                    return account.side
    
    def cep__compute_engaged_balance(self, account, cep_response):
        self.called_function_name="cep__compute_engaged_balance"
        if (account.balance != 0):
            account.engaged_balance = (account.positionAmt * account.entryPrice/account.balance)
            return 0
        else:
            print("WS should be restarting.\n{} \n {}. \
            ".format(cep_response, \
            account.exchange_platform_obj.CEP__GET_FUTURES_ACCOUNT_BALANCE( \
                                account.exchange_platform_obj.CEP__CLIENT( \
                                account.api_key._api_key, account.api_key._api_secret_key, None))))
            return 1