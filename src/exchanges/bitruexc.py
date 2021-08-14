from exchanges import exchange

import requests

class BitrueExchange(exchange.Exchange):

    def __init__(self):
        self._setName('Bitrue')
        self._setUrl('https://www.bitrue.com/api/v1/')

    def _responseOk(self, response) -> bool:
        if response == None:
            return False

        if response.status_code == 200:
            # check for json response
            # check for return code of 20000 in json
            return True
        else:
            print('There was a problem sending the request ({:s}) ({:d}).'.format(response.url, response.status_code))
            return False

    def getSymbols(self) -> dict:
        pass

    def getTime(self) -> dict:
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
