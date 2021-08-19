from data_streams import autoview
from data_streams import stream_publisher as sp
from exchanges import exchange
import json
import time
import threading

class TradeEngine(sp.StreamPublisher):

    def __init__(self, *streams):
        self.monitoredCoins = {}
        self._dataStreams = list(streams)
        self._dataMap = {}
        for stream in self._dataStreams:
            self._dataMap[stream.name] = {}
            stream.subscribe(self)

    def _constructSymbols(self):
        pass

    def update(self, data: dict): # this will be implemented as a thread
        print(f'data to update {data}')
        self._runAnalysis()

    def _runAnalysis(self):
        pass

if __name__ == '__main__':
    # pretend api
    av = autoview.AutoView()
    te = TradeEngine(av)

    av.setData({'message': 'hello, world!'});
