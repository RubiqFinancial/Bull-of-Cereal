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
        self._socket = 'wss://data.tradingview.com/socket.io/websocket'
        self.symbols = symbols
        # self.symbols = 'KUCOIN:BTCUSDT'
        self.quote_fields = fields;
        self._websocket_thread = None

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
    def _generate_session(self):
        string_length = 12
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(string_length))
        return "qs_" + random_string

    # generates chart session id string
    def _generate_chart_session(self):
        string_length = 12
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(string_length))
        return "cs_" + random_string

    def _prepend_header(self, st):
        return "~m~" + str(len(st)) + "~m~" + st

    def _construct_message(self, func, param_list):
        #json_mylist = json.dumps(mylist, separators=(',', ':'))
        return json.dumps({
            "m": func,
            "p": param_list
        }, separators=(',', ':'))

    # creates message to be sent through websocket
    def _create_message(self, func, param_list):
        return self._prepend_header(self._construct_message(func, param_list))

    # sends message through websocket
    def _send_message(self, ws, func, args):
        ws.send(self._create_message(func, args))
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

        session = self._generate_session()
        # print(f"session generated {session}")

        chart_session = self._generate_chart_session()
        # print("chart_session generated {}".format(chart_session))

        self._send_message(ws, "set_auth_token", ['unauthorized_user_token'])

        self._send_message(ws, "chart_create_session", [chart_session]) # create a chart session stream
        self._send_message(ws, "quote_create_session", [session]) # create a quote session stream
        #
        # quote fields to be returned
        fields = self.quote_fields.copy()
        fields.insert(0, session)
        self._send_message(ws, "quote_set_fields", fields)

        p_symbols = self.symbols.copy()
        # pSymbols = [self.symbols]
        p_symbols.insert(0, session)
        self._send_message(ws, "quote_add_symbols", p_symbols)
        # print(self.symbols)

        # self._sendMessage(ws, 'resolve_symbols', [chart_session, 'sds_sym1', self.symbols])
        # ws.send('~m~144~m~{"m":"resolve_symbol","p":["cs_1fufbON7frBP","sds_sym_1","={\"symbol\":\"KUCOIN:BTCUSDT\",\"adjustment\":\"splits\",\"session\":\"extended\"}"]}')
        # self._sendMessage(ws, 'create_series', [chart_session, 'sds_1', 's1', 'sds_sym1', '60', 300, ''])


    def create_web_socket(self, on_message=None, on_error=None, on_close=None):
        on_message = self.on_message if on_message == None else on_message
        on_error = self.on_error if on_error == None else on_error
        on_close = self.on_close if on_close == None else on_close

        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(self._socket,
                                    on_open=self.on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)

        return ws
