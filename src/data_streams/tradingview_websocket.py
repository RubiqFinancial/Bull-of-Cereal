# Author: Michael Lauderback
# references work from https://gist.github.com/algo2t/34f4462f6e8670249f7c58545eb83db4
from trade_engine import coin, candle
from exchanges import exchange
import websocket
import time
import threading
import json
import string
import random
import re
import asyncio
import requests

class TradingViewWebSocket:

    def __init__(self, symbols, fields):
        self._SOCKET = 'wss://data.tradingview.com/socket.io/websocket'
        self.symbols = symbols
        self.quoteFields = fields;
        self._websocketThread = None

    def filter_raw_message(self, text):
        try:
            found1 = re.search('"m":"(.+?)",', text).group(1)
            found2 = re.search('"p":(.+?"}"])}', text).group(1)
            print(found1)
            print(found2)
            return found1, found2
        except AttributeError:
            print("error")

    # generates session id string
    def _generateSession(self):
        stringLength = 12
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(stringLength))
        return "qs_" + random_string

    # generates chart session id string
    def _generateChartSession(self):
        stringLength = 12
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(stringLength))
        return "cs_" + random_string

    def _prependHeader(self, st):
        return "~m~" + str(len(st)) + "~m~" + st

    def _constructMessage(self, func, paramList):
        #json_mylist = json.dumps(mylist, separators=(',', ':'))
        return json.dumps({
            "m": func,
            "p": paramList
        }, separators=(',', ':'))

    # creates message to be sent through websocket
    def _createMessage(self, func, paramList):
        return self._prependHeader(self._constructMessage(func, paramList))

    # sends message through websocket
    def _sendMessage(self, ws, func, args):
        ws.send(self._createMessage(func, args))
        # print(self._createMessage(func, args))

    def on_message(self, ws, message):
        print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print('connection closed')

    # ~m~82~m~{"m":"create_series","p":["cs_b2EjbnYrDjOY","sds_1","s1","sds_sym_1","1W",300,""]}
    def on_open(self, ws):
        print('Opened new connection.')

        session = self._generateSession()
        # print(f"session generated {session}")

        chart_session = self._generateChartSession()
        # print("chart_session generated {}".format(chart_session))

        # token = self._generateAuthToken()
        # self._sendMessage(ws, "set_auth_token", [token]) # set connection permissions
        # print(token)
        self._sendMessage(ws, "set_auth_token", ['unauthorized_user_token'])

        self._sendMessage(ws, "chart_create_session", [chart_session]) # create a chart session stream
        self._sendMessage(ws, "quote_create_session", [session]) # create a quote session stream
        #
        # quote fields to be returned
        fields = self.quoteFields.copy()
        fields.insert(0, session)
        self._sendMessage(ws, "quote_set_fields", fields)

        pSymbols = self.symbols.copy()
        pSymbols.insert(0, session)
        self._sendMessage(ws, "quote_add_symbols", pSymbols)


    def createWebSocket(self, on_message=None, on_error=None, on_close=None):
        on_message = self.on_message if on_message == None else on_message
        on_error = self.on_error if on_error == None else on_error
        on_close = self.on_close if on_close == None else on_close

        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(self._SOCKET,
                              on_open=self.on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

        return ws
