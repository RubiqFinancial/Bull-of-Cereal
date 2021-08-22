from data_streams import tradingview_websocket
from data_streams import stream_publisher as sp
from data_streams import stream_subscriber as ss
import threading
import json
import time

class VolumeStream(sp.StreamPublisher):

    def __init__(self, monitored_coins: dict):
        super().__init__()
        self.name = 'VolumeMonitor'
        self._data = {'stream': self.name}
        self.symbols = []
        self._last_message = {}
        self.web_socket = None

        # adjust coin symbol for the websocket params
        for coin in monitored_coins:
            name = coin.get_symbol().replace(':','')
            self.symbols.append(f'{coin.exchange}:{name}')

        self.fields = ['volume']
        # self.fields = ["ch", "chp", "current_session", "description", "local_description",
        #      "language", "exchange", "fractional", "is_tradable", "lp", "lp_time", "minmov",
        #      "minmove2","original_name", "pricescale", "pro_name", "short_name", "type",
        #      "update_mode", "volume","rchp", "rtc", "rtc_time", "currency_code"]
        self.tvws = tradingview_websocket.TradingViewWebSocket(self.symbols, self.fields)

    def add_subscriber(self, subscriber: ss.StreamSubscriber):
        self._subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: ss.StreamSubscriber):
        self._subscribers.remove(subscriber)

    def notify(self):
        for subscriber in self._subscribers:
            subscriber.update(self._data)

    # must invoke as daemon thread
    def set_data(self, new_data: dict):
        new_keys = list(new_data)
        for key in new_keys:
            self._data[key] = new_data[key]

        self.notify()

    def _on_message(self, ws, message):
        p = message.split('~', -1)[4]
        data = json.loads(p)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        symbol = data['p'][1]['n']
        volume = data['p'][1]['v']['volume']
        # filter data here

        new_data = {
            'symbol': symbol,
            'volume': volume,
            'time': timestamp
        }
        self.set_data(new_data)
        self._last_message = data
        # print(message)

    def _on_close(self, ws, status_code, message):

        print(f'code: {status_code}, message: {message}')
        if status_code == 1000 and message == '':
            if self._last_message['m'] == 'protocol_error':
                print('There was a problem... closing the connection')
                return

            print('creating new websocket connection')
            self.restart_stream()

        if status_code == None and message == None:
            print('connection closed unexpectedly')

    def init_stream(self):
        self.web_socket = self.tvws.create_web_socket(on_message=self._on_message, on_close=self._on_close)
        self.web_socket.run_forever()

    def restart_stream(self):
        self.web_socket.close()
