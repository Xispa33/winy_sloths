#!/bin/bash
export PYTHONPATH=$PWD/../../

MAIN_DIR=../..
UTILS_DIR=$MAIN_DIR/utils

API_KEY='EYoXqgORlsC2q15AwiK30swZIBdrc1PVZZhMIoZlWEFUstIum0LdCPEm3eG7cF5y'
API_SECRETKEY='6hbXJ5kc9yRBl3VIHtKheQ0h6Fe5eG05cC99X3lBy5CzQvpBLUL4F1OkvyzhNRta'

python3 ${UTILS_DIR}/open_long.py -k ${API_KEY} ${API_SECRETKEY} -t SPOT -s BTCUSDT
#python3 ${UTILS_DIR}/get_account_info.py -k ${API_KEY} ${API_SECRETKEY} -t S -s BTCUSDT