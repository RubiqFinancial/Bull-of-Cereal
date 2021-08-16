import tradingview_ta as tv

class TradeEngine:

    def __init__(self):
        self._handler = tv.TA_Handler(
            symbol="",
            exchange="binance",
            screener="crypto",
            interval="",
            timeout=None
        )

    def querySymbol(self, symbol: str) -> tv.main.Analysis:
        self._handler.symbol = symbol
        self._handler.interval = tv.Interval.INTERVAL_1_HOUR

        analysis = self._handler.get_analysis()
        return analysis
