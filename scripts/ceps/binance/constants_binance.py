#!/usr/bin/python3
# -*- coding: utf-8 -*-

SECURITY_TYPE_NONE = "NONE"
SECURITY_TYPE_TRADE = "TRADE"	#Endpoint requires sending a valid API-Key and signature.
SECURITY_TYPE_MARGIN = "MARGIN"	#Endpoint requires sending a valid API-Key and signature.
SECURITY_TYPE_USER_DATA	= "USER_DATA" #Endpoint requires sending a valid API-Key and signature.
SECURITY_TYPE_USER_STREAM = "USER_STREAM"	#Endpoint requires sending a valid API-Key.
SECURITY_TYPE_MARKET_DATA = "MARKET_DATA"
SERVER_TIME_ENDPOINT = ("/fapi/v1/time", SECURITY_TYPE_NONE)
FUTURES_POSITION_INFORMATION = ("/fapi/v2/positionRisk", SECURITY_TYPE_USER_DATA)
FUTURES_ACCOUNT_BALANCE = ("/fapi/v2/balance", SECURITY_TYPE_USER_DATA)
FUTURES_CHANGE_POSITION_MODE = ("/fapi/v1/positionSide/dual", SECURITY_TYPE_TRADE)
FUTURES_CHANGE_LEVERAGE = ("/fapi/v1/leverage", SECURITY_TYPE_TRADE)
FUTURES_TICKER_PRICE = ("/fapi/v1/ticker/price", SECURITY_TYPE_NONE)
FUTURES_POSITION_MODE = ("/fapi/v1/positionSide/dual", SECURITY_TYPE_USER_DATA)
FUTURES_CREATE_ORDER = ("/fapi/v1/order", SECURITY_TYPE_TRADE)
SERVER_TIME = "serverTime"
CODE = "code"
SIGNATURE = "signature"
X_MBX_APIKEY = 'X-MBX-APIKEY'
NOTIONAL = 'notional'
DUAL_SIDE_POSITION = 'dualSidePosition'
QUANTITY = 'quantity'
LIMIT = 'limit'
QUOTE_ORDER_QTY = 'quoteOrderQty'
SPOT_GET_ALL_ORDERS = ('/api/v3/allOrders', SECURITY_TYPE_USER_DATA)
SPOT_GET_AVG_PRICE = ('/api/v3/avgPrice', SECURITY_TYPE_NONE)
SPOT_SYMBOL_PRICE_TICKER = ('/api/v3/ticker/price', SECURITY_TYPE_NONE)
SPOT_SYMBOL_ORDER_BOOK = ('/api/v3/depth', SECURITY_TYPE_NONE)
SPOT_AGGREGATES_TRADES = ('/api/v3/aggTrades', SECURITY_TYPE_NONE)
SPOT_GET_ASSET_BALANCE = ('/api/v3/account', SECURITY_TYPE_USER_DATA)
SPOT_CREATE_ORDER = ('/api/v3/order',SECURITY_TYPE_TRADE)
SPOT_GET_EXCHANGE_INFO = ('/api/v3/exchangeInfo', SECURITY_TYPE_NONE)
START_TIME = 'startTime'
END_TIME = 'endTime'
BALANCES = 'balances'