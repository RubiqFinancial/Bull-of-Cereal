from data_streams import volumestream, tradingview
from exchanges import exchange
from stream_publisher import StreamPublisher
import json
import time
import threading

class TradeEngine(StreamPublisher):

    def __init__(self, *streams):
        self.monitoredCoins = {}
        self._dataStreams = list(streams)
        self._dataMap = {}
        for stream in self._dataStreams:
            self._dataMap[stream.name] = {}
            stream.registerObserver(self)

    def _constructSymbols(self):
        pass

    def update(self, data: dict): # this will be implemented as a thread
        
        self._runAnalysis()

    def _runAnalysis(self):
        pass
