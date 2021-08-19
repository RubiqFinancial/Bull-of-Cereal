from data_streams import autoview, volumestream
from data_streams import stream_subscriber as ss
from exchanges.exchange import Exchange
from trade_engine.coin import Coin
from trade_engine import candle
import json
import time
import threading

class TradeEngine(ss.StreamSubscriber):

    def __init__(self):
        self.monitoredCoins = [
            Coin(Coin.BTC, Coin.USDT, Exchange.KUCOIN),
            Coin(Coin.ETH, Coin.USDT, Exchange.KUCOIN)
        ]
        # print(self.monitoredCoins[0].candles[candle.Interval.FIFTEEN_MINUTE].high)
        self._dataStreams = []
        self._dataMap = {}

    def addPublishers(self, *publishers):
        for stream in publishers:
            self._dataMap[stream.name] = {}
            stream.addSubscriber(self)

    # This method should be called as a thread because it is not thread safe
    # and could be called by another publisher
    def update(self, data: dict):
        # TODO: implement mutex locking here
        print(f'data to update {data}')
        self._runAnalysis()
        # mutex unlocks here.  unlocking before could mess up shared data
        # for the analysis

    def _runAnalysis(self):
        pass

    def isMonitoredCoin(self, coin: Coin) -> bool:
        pass

if __name__ == '__main__':
    # pretend api
    te = TradeEngine()
    av = autoview.AutoView()
    vm = volumestream.VolumeStream(te.monitoredCoins)
    te.addPublishers(av, vm)

    avThread = threading.Thread(target=av.setData({'message': 'hello, world!'}), daemon=True)
    vm.stream() # automatically creates thread
    avThread.start()
