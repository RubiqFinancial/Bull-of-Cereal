class ExchangePool:
    # a data structure that keeps track of all coin exchanges

    def __init__(self, exchanges={}):
        self._exchanges = exchanges

    def add_exchange(self, name, exchange):
        self._exchanges[name] = exchange;

    def remove_exchange(self, exchangeName):
        if exchangeName in self._exchanges:
            del self._exchanges[exchangeName]

    def get_exchanges(self):
        return self._exchanges

    def queryAllExchanges(self):
        if len(self._exchanges) == 0:
            print('ERROR: No exchanges listed.')
            return
