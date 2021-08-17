import tradingview_ta as tva
import threading
import time
import datetime
import asyncio

class TradingView:

    def __init__(self):
        self._handler = tva.TA_Handler(screener='crypto', interval=tva.Interval.INTERVAL_1_MINUTE, timeout=2)

    def getSymbolInfo(self, symbol: str, exchange: str) -> tva.main.Analysis:
        self._handler.symbol = symbol
        self._handler.exchange = exchange
        return self._handler.get_analysis()

    def getMultipleSymbolInfo(self, symbols: list) -> dict:
        print(symbols)
        return tva.get_multiple_analysis(screener=self._handler.screener, interval=self._handler.interval, symbols=symbols)

    def pollSymbols(self, pollSymbols: list):
        while True:
            analysis = self.getMultipleSymbolInfo(pollSymbols)
            symbols = list(analysis.keys())
            info = list(analysis.values())
            print(f'Time: {datetime.datetime.utcnow()}')
            for i in range(0, len(symbols)):
                print(f'{symbols[i]}: {info[i].summary}')
            print('----------')
            time.sleep(10)
