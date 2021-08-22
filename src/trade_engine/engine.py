from data_streams import autoview, volumestream
from data_streams import stream_subscriber as ss
from exchanges.exchange import Exchange, ExchangeName
from trade_engine import candle, coin
import json
import time
import threading

class TradeEngine(ss.StreamSubscriber):

    def __init__(self):
        self.monitored_coins = [
            coin.Coin(coin.Currency.BTC, coin.Currency.USDT, ExchangeName.KUCOIN),
            coin.Coin(coin.Currency.ETH, coin.Currency.USDT, ExchangeName.KUCOIN)
        ]
        # print(self.monitoredCoins[0].candles[candle.Interval.FIFTEEN_MINUTE].high)
        self._data_streams = []
        self._data_map = {}

    def add_publishers(self, *publishers):
        for stream in publishers:
            self._data_map[stream.name] = {}
            stream.add_subscriber(self)

    # This method should be called as a thread because it is not thread safe
    # and could be called by another publisher
    def update(self, data: dict):
        # TODO: implement mutex locking here
        print(f'data to update {data}')
        self._run_analysis()
        # mutex unlocks here.  unlocking before could mess up shared data
        # for the analysis

    def _run_analysis(self):
        pass

    def is_monitored_coin(self, coin: coin.Coin) -> bool:
        pass

if __name__ == '__main__':
    # pretend api
    te = TradeEngine()
    av = autoview.AutoView()
    vm = volumestream.VolumeStream(te.monitored_coins)
    te.add_publishers(av, vm)

    # avThread = threading.Thread(target=av.setData({'message': 'hello, world!'}), daemon=True)
    vm.init_stream() # automatically creates thread
    # avThread.start()
