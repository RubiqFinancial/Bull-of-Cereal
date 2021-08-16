import exchange, kucoinxc, bitruexc, exchangepool

class ExchangeManager:

    def __init__(self):
        self._exchangePool = exchangepool.ExchangePool([
            kucoinxc.KucoinExchange(),
            bitruexc.BitrueExchange()
        ])

    def getExchanges(self) -> list:
        return self._exchangePool.getExchanges()

    def getExchange(self, exchange: str) -> exchange.Exchange:
        exchange = exchange.lower()
        return self._exchangePool.getExchange(exchange)
