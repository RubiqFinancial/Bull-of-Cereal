from exchanges import exchange

import requests

class BitrueExchange(exchange.Exchange):

    def __init__(self):
        self.setName('Bitrue')
        self.setUrl('https://www.bitrue.com/api/v1/')

    def getSymbols(self) -> dict:
        pass

    async def getTime(self) -> dict:
        endpoint = 'time'
        # this server reports UTC time
        response = requests.get(self.getUrl() + endpoint)
        if not self._responseOk(response):
            return None

        return response.json()

    def getSymbolPrice(self, symbol) -> dict:
        pass

    def getHistoricalData(self, symbol, interval, start, limit) -> dict:
        pass

    def getAccountInfo(self) -> dict:
        pass
