import requests

class BitrueExchange:

    def __init__(self):
        self.namestr = 'Bitrue'
        self._url = 'https://www.bitrue.com/api/v1/'
        self._endpoint = ''

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

    def getSymbols(self) -> requests.Response:
        pass

    def getTime(self) -> requests.Response:
        pass

    def getSymbolPrice(self, symbol) -> requests.Response:
        pass

    def getHistoricalData(self, symbol, interval, start, limit) -> requests.Response:
        pass

    def getAccountInfo(self) -> requests.Response:
        pass
