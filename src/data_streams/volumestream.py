from data_streams import tradingview_websocket
from data_streams import stream_publisher as sp
from data_streams import stream_subscriber as ss
import threading
import json
import time

class VolumeStream(sp.StreamPublisher):

    def __init__(self, monitoredCoins: dict):
        super().__init__()
        self.name = 'VolumeMonitor'
        self._data = {'stream': self.name}
        self.symbols = []

        # adjust coin symbol for the websocket params
        for coin in monitoredCoins:
            name = coin.getSymbol().replace(':','')
            self.symbols.append(f'{coin.exchange}:{name}')

        # self.fields = ['volume']
        self.fields = ["ch", "chp", "current_session", "description", "local_description",
             "language", "exchange", "fractional", "is_tradable", "lp", "lp_time", "minmov",
             "minmove2","original_name", "pricescale", "pro_name", "short_name", "type",
             "update_mode", "volume","rchp", "rtc", "rtc_time", "currency_code"]
        self.tvws = tradingview_websocket.TradingViewWebSocket(self.symbols, self.fields)

    def addSubscriber(self, subscriber: ss.StreamSubscriber):
        self._subscribers.append(subscriber)

    def removeSubscriber(self, subscriber: ss.StreamSubscriber):
        self._subscribers.remove(subscriber)

    def notify(self):
        for subscriber in self._subscribers:
            subscriber.update(self._data)

    # must invoke as daemon thread
    def setData(self, newData: dict):
        newKeys = list(newData)
        for key in newKeys:
            self._data[key] = newData[key]

        self.notify()

    def _on_message(self, ws, message):
        p = message.split('~', -1)[4]
        data = json.loads(p)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        symbol = data['p'][1]['n']
        volume = data['p'][1]['v']['volume']

        # filter data here

        newData = {
            'symbol': symbol,
            'volume': volume,
            'time': timestamp
        }
        # self.setData(newData)
        print(message)
        # print(f'tick :timestamp: {timestamp} :symbol: {symbol} :volume: {volume}')

    def _on_close(self, ws, status_code, message):
        # print('connection closed')
        # print(f'code: {status_code}, message: {message}')
        if status_code == 1000 and message == '':
            print('creating new websocket connection')
            self.stream()

        if status_code == None and message == None:
            print('connection closed unexpectedly')

    def stream(self):
        # set this up to reconnect on lost connection
        ws = self.tvws.createWebSocket(on_message=self._on_message, on_close=self._on_close)
        wsThread = threading.Thread(target=ws.run_forever(), args=(), daemon=True)
        wsThread.start()
        wsThread.join()
