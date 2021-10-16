#!/usr/bin/python3
# -*- coding: utf-8 -*-

BALANCES = "balances"
BUY = "Buy"
COIN = 'coin'
MARKET = "Market"
SELL = "Sell"
ENTRY_PRICE = "entry_price"
POSITION_VALUE = "position_value"
POSITION_MARGIN = "position_margin"
BYBIT_SERVER_TIME_ENDPOINT = "/v2/public/time"
BYBIT_SPOT_ORDER_HISTORY = "/spot/v1/history-orders"
BYBIT_SPOT_WALLET_BALANCE = "/spot/v1/account"
BYBIT_SPOT_CREATE_ORDER = "/spot/v1/order"
BYBIT_SPOT_SYMBOL_PRICE = "/spot/quote/v1/ticker/price"
BYBIT_SPOT_SYMBOL_LAST_TRADE_PRICE = "/spot/quote/v1/ticker/price"
BYBIT_SPOT_SYMBOL_PRICE_TICKER = "/spot/quote/v1/ticker/24hr"
BYBIT_SPOT_SYMBOL_ORDER_BOOK = "/spot/quote/v1/depth"
BYBIT_SPOT_QUERY_SYMBOL = "/spot/v1/symbols"
TIME_NOW = 'time_now'
RET_CODE = "ret_code"
GET = "get"
POST = "post"
API_KEY = "api_key"
SIGN = "sign"
LIMIT = "limit"
QTY = "qty"

BYBIT_FUTURES_WALLET_BALANCE = "/v2/private/wallet/balance"
BYBIT_FUTURES_POSITION = "/private/linear/position/list"
BYBIT_FUTURES_SYMBOL_LASTEST_INFO = "/v2/public/tickers"
BYBIT_FUTURES_PLACE_ORDER = "/private/linear/order/create"
BYBIT_FUTURES_MY_POSITIONS = "/private/linear/position/list"
BYBIT_FUTURES_SET_LEVERAGE = "/private/linear/position/set-leverage"
BYBIT_DEFAULT_LEVERAGE = 10
BYBIT_MAX_LEVERAGE = 18