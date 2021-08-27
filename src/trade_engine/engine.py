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

    def is_monitoring(self, coin) -> bool: # coin can be the name string or a Coin object
        if coin is None:
            return False

        if type(coin) == str:
             for monitored_coin in self.monitored_coins:
                 if coin == monitored_coin.get_symbol_string():
                    return True

        if type(coin) == coin.Coin:
            if coin in self.monitored_coins:
                return True

        print('ERROR: coin cannot be read.  Returning False')
        return False

    def get_json(self):
        return {
            'coins': self.monitored_coins,
            'streams': self._data_streams,
            'map': self._data_map
        }


if __name__ == '__main__':
    # pretend api
    te = TradeEngine()
    av = autoview.Autoview()
    vm = volumestream.VolumeStream(te.monitored_coins)
    te.add_publishers(av, vm)

    # avThread = threading.Thread(target=av.setData({'message': 'hello, world!'}), daemon=True)
    # avThread.start()
    vmThread = threading.Thread(target=vm.init_stream(), daemon=True)
    vmThread.start()
    print("hello, world!")
