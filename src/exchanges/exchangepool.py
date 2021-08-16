import exchange

class ExchangePool:

    def __init__(self, exchanges=[]):
        self._exchanges = exchanges

    def addExchange(self, exchange: exchange.Exchange):
        self._exchanges.append(exchange)

    def removeExchange(self, exchangeName: str) -> bool:
        if exchangeName in self._exchanges:
            del self._exchanges[exchangeName]
            return True
        return False

    def getExchanges(self) -> list:
        return self._exchanges

    def getExchange(self, exchange: str) -> exchange.Exchange:
        for xc in self._exchanges:
            if xc.getName().lower() == exchange.lower():
                return xc

        return None

    async def compareExchangePrices(symbol: str, exchanges=[]) -> dict:
        if not bool(exchanges):
            exchanges = self._exchanges
