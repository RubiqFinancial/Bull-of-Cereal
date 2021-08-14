from exchanges import exchange

class ExchangePool:

    def __init__(self, exchanges={}):
        self._exchanges = exchanges

    def addExchange(self, name: str, exchange: exchange.Exchange):
        self._exchanges[name] = exchange;

    def removeExchange(self, exchangeName: str):
        if exchangeName in self._exchanges:
            del self._exchanges[exchangeName]

    def getExchanges(self) -> dict:
        return self._exchanges

    async def compareExchangePrices(symbol: str, exchanges={}) -> dict:
        if not bool(exchanges):
            exchanges = self._exchanges
