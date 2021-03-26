#!/usr/bin/python3
# -*- coding: utf-8 -*-

SPOT = 'SPOT'
FUTURES = 'FUTURES'
UNDEFINED = 'UNDEFINED'
BUY = 'BUY'
SELL = 'SELL'
OUT = 'OUT'
BOTH = 'BOTH'
LONG = 'LONG'
SHORT = 'SHORT'
VALID_KEY = 0
NOT_VALID_KEY = 1
TREE_FILE = "history.txt"
REALIZED_PNL = 'realizedPnl'
ID = 'id'
QTY = 'qty'
ORIGQTY = 'origQty'
TIME = 'time'
ORDER_ID = 'orderId'
SYMBOL = 'symbol'
PRICE = 'price'
SIDE = 'side'
TYPE = 'type'
CURRENT_SIDE = 'current_side'
NA = 'NA'
NO_C = 0
INFO_C = 1
MEDIUM_C = 2
HIGH_C = 3
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"
CORRESPONDANCE_DICT = {INFO_C:"INFO", MEDIUM_C:"WARNING", HIGH_C: "ERROR"}
MAX_RETRY = 5
MAX_KO_STRATEGY = 3

#EMAIL CONSTANTS
PORT = 465
RECEIVERS = ['briceleal@hotmail.fr'] 
EMITTOR = 'towardsecolonomy@gmail.com'
STMP_URL = "smtp.gmail.com"
EMITTOR_PASSWORD = 'ricqltndktzitayp'
ALTERNATIVE = 'alternative'
SUBJECT = 'Subject'
FROM = 'From'
TO = 'To'
PLAIN = 'plain'
