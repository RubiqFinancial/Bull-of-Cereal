import datetime
import pandas as pd
import re
import os
import math
from dateutil.parser import parse
from datetime import timedelta
import numpy as np
from tqdm import tqdm
import datetime
import logging
from logging import Handler, Formatter
import time
import requests
import warnings
import config_file

warnings.filterwarnings('ignore')

from binance.client import Client

def exchange_info(client):
    data = client.futures_exchange_info()['symbols']
    return data

def get_trading_rules(symbol, data):
    d = list(filter(lambda coin: coin['symbol'] == symbol, data))
    # print(d)
    filter_data = d[0]['filters']
    p = list(filter(lambda coin: coin['filterType'] == 'PRICE_FILTER', filter_data))
    q = list(filter(lambda coin: coin['filterType'] == 'LOT_SIZE', filter_data))
    return float(p[0]['tickSize']), float(q[0]['stepSize'])

def correct_precision(num, prec):
    val = round(num, find_decimals(prec))
    return val
    # return (num // prec) * prec

def find_decimals(num):
    n = num
    count = 0
    while n < 1:
        n = n * 10
        count+=1
    return count

def get_historical_data(client, symbol, interval, start, limit):
    columns = [
        'Open_time',
        'open',
        'high',
        'low',
        'close',
        'volume',
        'Close_time',
        'Quote_asset_volume',
        'Number_of_trades',
        'Taker_buy_base_asset_volume',
        'Taker_buy_quote_asset_volume',
        'Ignore',
      ]
    data = client.futures_klines(symbol=symbol, interval=interval, startTime=start, limit=limit)
    temp_df = pd.DataFrame(np.array(data), columns=columns)
    temp_df['Open_time'] = temp_df['Open_time'].apply(lambda x: pd.Timestamp(int(x), unit='ms'))
    temp_df['Close_time'] = temp_df['Close_time'].apply(
        lambda x: pd.Timestamp(int(x), unit='ms'))

    temp_df['Open_time'] = pd.to_datetime(temp_df['Open_time'])

    temp_df['open'] = temp_df['open'].astype(float)
    temp_df['high'] = temp_df['high'].astype(float)
    temp_df['low'] = temp_df['low'].astype(float)
    temp_df['close'] = temp_df['close'].astype(float)
    temp_df['volume'] = temp_df['volume'].astype(float)
    return temp_df



# function to convert entered timeframe value to minutes
def extract_digits(text):
    RX_INTERVAL = re.compile(r'(\d+)(\w)')
    num, dur = RX_INTERVAL.findall(text)[0]
    num = int(num)
    intervals = dict(
        m=1,
        h=60,
        d=1440,
        w=10080
    )
    minutes = num * intervals[dur]
    return minutes


def place_market_sell_order(client, symbol, qty, reduceOnly=False):
    return client.futures_create_order(symbol=symbol,
                                    side=Client.SIDE_SELL,
                                    type="MARKET",
                                    reduceOnly = reduceOnly,
                                    quantity=qty)



def place_market_buy_order(client, symbol, qty, reduceOnly=False):
    return client.futures_create_order(symbol=symbol,
                                    side=Client.SIDE_BUY,
                                    type="MARKET",
                                    reduceOnly=reduceOnly,
                                    quantity=qty)

def place_stop_sell_order(client, symbol, price, qty, reduceOnly=False, workingType='CONTRACT_PRICE', priceProtect=False, closePosition=False):
    return  client.futures_create_order(symbol=symbol,
                                        side=Client.SIDE_SELL,
                                        type="STOP_MARKET",
                                        stopPrice=price,
                                        reduceOnly=reduceOnly,
                                        workingType=workingType,
                                        priceProtect=priceProtect,
                                        closePosition=closePosition,
                                        quantity=qty)


def place_stop_buy_order(client,symbol, price, qty, reduceOnly=False, workingType='CONTRACT_PRICE', priceProtect=False, closePosition=False):
    return  client.futures_create_order(symbol=symbol,
                                        side=Client.SIDE_BUY,
                                        type="STOP_MARKET",
                                        stopPrice=price,
                                        reduceOnly=reduceOnly,
                                        workingType=workingType,
                                        priceProtect=priceProtect,
                                        closePosition=closePosition,
                                        quantity=qty)


def place_take_profit_sell_order(client, symbol, price, qty, reduceOnly=False, workingType='CONTRACT_PRICE', priceProtect=False, closePosition=False):
    return  client.futures_create_order(symbol=symbol,
                                        side=Client.SIDE_SELL,
                                        type="TAKE_PROFIT_MARKET",
                                        stopPrice=price,
                                        reduceOnly=reduceOnly,
                                        workingType=workingType,
                                        priceProtect=priceProtect,
                                        closePosition=closePosition,
                                        quantity=qty)


def place_take_profit_buy_order(client, symbol, price, qty, reduceOnly=False, workingType='CONTRACT_PRICE', priceProtect=False, closePosition=False):
    return  client.futures_create_order(symbol=symbol,
                                        side=Client.SIDE_BUY,
                                        type="TAKE_PROFIT_MARKET",
                                        stopPrice=price,
                                        reduceOnly=reduceOnly,
                                        workingType=workingType,
                                        priceProtect=priceProtect,
                                        closePosition=closePosition,
                                        quantity=qty)

def place_limit_sell_order(client, symbol, price, qty, reduceOnly=False, tif = "GTC"):
    return client.futures_create_order(symbol=symbol,
                                    side=Client.SIDE_SELL,
                                    type="LIMIT",
                                    reduceOnly = reduceOnly,
                                    timeInForce = tif,
                                    price=price,
                                    quantity=qty)



def place_limit_buy_order(client, symbol, price, qty, reduceOnly=False, tif = "GTC"):
    return client.futures_create_order(symbol=symbol,
                                    side=Client.SIDE_BUY,
                                    type="LIMIT",
                                    reduceOnly=reduceOnly,
                                    timeInForce=tif,
                                    price=price,
                                    quantity=qty)

def place_stop_limit_sell_order(client, symbol, price, trigger, qty, reduceOnly=False, workingType='CONTRACT_PRICE', priceProtect=False, tif="GTC"):
    return  client.futures_create_order(symbol=symbol,
                                        side=Client.SIDE_SELL,
                                        type="STOP",
                                        timeInForce=tif,
                                        price=price,
                                        stopPrice=trigger,
                                        reduceOnly=reduceOnly,
                                        workingType=workingType,
                                        priceProtect=priceProtect,
                                        quantity=qty)


def place_stop_limit_buy_order(client, symbol, price, trigger, qty, reduceOnly=False, workingType='CONTRACT_PRICE', priceProtect=False, tif="GTC"):
    return  client.futures_create_order(symbol=symbol,
                                        side=Client.SIDE_BUY,
                                        type="STOP",
                                        timeInForce=tif,
                                        price=price,
                                        stopPrice=trigger,
                                        reduceOnly=reduceOnly,
                                        workingType=workingType,
                                        priceProtect=priceProtect,
                                        quantity=qty)


def place_take_profit_limit_sell_order(client, symbol, price, trigger, qty, reduceOnly=False, workingType='CONTRACT_PRICE', priceProtect=False, tif="GTC"):
    return  client.futures_create_order(symbol=symbol,
                                        side=Client.SIDE_SELL,
                                        type="TAKE_PROFIT",
                                        timeInForce=tif,
                                        price=price,
                                        stopPrice=trigger,
                                        reduceOnly=reduceOnly,
                                        workingType=workingType,
                                        priceProtect=priceProtect,
                                        quantity=qty)


def place_take_profit_limit_buy_order(client, symbol, price, trigger, qty, reduceOnly=False, workingType='CONTRACT_PRICE', priceProtect=False, tif="GTC"):
    return  client.futures_create_order(symbol=symbol,
                                        side=Client.SIDE_BUY,
                                        type="TAKE_PROFIT",
                                        timeInForce=tif,
                                        price=price,
                                        stopPrice=trigger,
                                        reduceOnly=reduceOnly,
                                        workingType=workingType,
                                        priceProtect=priceProtect,
                                        quantity=qty)


def cancel_order(client, symbol, orderid):
    return client.futures_cancel_order(symbol=symbol, orderId=orderid)

def cancel_all_orders(client, symbol):
    return client.futures_cancel_all_open_orders(symbol=symbol)

def get_order_status(client, symbol, orderid):
    return client.futures_get_order(symbol=symbol, orderId =orderid)

def get_futures_account_balance(client):
    return client.futures_account_balance()

def change_margin(client, symbol, marginType="CROSSED"):
    return client.futures_change_margin_type(symbol=symbol, marginType=marginType)

def change_leverage(client, symbol, leverage):
    return client.futures_change_leverage(symbol=symbol, leverage=leverage)

def change_position_margin(client, symbol, positionSide, amount, type):
    return client.futures_change_position_margin(symbol=symbol, positionSide=positionSide, amount=amount, type=type)


if __name__ == '__main__':
    client = Client(api_key=config_file.accounts['binance']['a1']['api_key'],
                    api_secret=config_file.accounts['binance']['a1']['api_secret'])

    rules = client.futures_exchange_info()['symbols']

    pp, qp = get_trading_rules("BTCUSDT", rules)