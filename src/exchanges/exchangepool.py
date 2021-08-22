from exchanges import exchange

class ExchangePool:

    def __init__(self, exchanges=[]):
        self._exchanges = exchanges

    def add_exchange(self, exchange: exchange.Exchange):
        self._exchanges.append(exchange)

    def remove_exchange(self, exchange_name: exchange.ExchangeName) -> bool:
        if exchange_name.name in self._exchanges:
            del self._exchanges[exchange_name]
            return True
        return False

    def get_exchanges(self) -> list:
        return self._exchanges

    def get_exchange(self, exchange_name: exchange.ExchangeName) -> exchange.Exchange:
        for xc in self._exchanges:
            if xc.get_name() == exchange_name:
                return xc

        return None

    async def compare_exchange_prices(symbol: str, exchanges=[]) -> dict:
        if not bool(exchanges):
            exchanges = self._exchanges
