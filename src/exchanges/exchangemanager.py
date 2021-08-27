from exchanges import exchange, kucoinxc, bitruexc, exchangepool


class ExchangeManager:

    def __init__(self):
        self._exchange_pool = exchangepool.ExchangePool([ # change exchange pool constructor to use *args notation
            kucoinxc.KucoinExchange(),
            bitruexc.BitrueExchange()])

    def add_exchange(self, exchange: exchange.Exchange) -> None:
        self._exchange_pool.add_exchange(exchange)

    def remove_exchange(self, exchange: exchange.Exchange) -> bool:
        return self._exchange_pool.remove_exchange(exchange)

    def get_exchanges(self) -> list:
        return self._exchange_pool.get_exchanges()

    def get_exchange(self, exchange: exchange.ExchangeName) -> exchange.Exchange:
        return self._exchange_pool.get_exchange(exchange)
