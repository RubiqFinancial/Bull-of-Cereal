from exchanges import exchange

import hashlib
import hmac
import base64
import requests
import re
import time

class KucoinExchange(exchange.Exchange):

    def __init__(self):
        self._setName('Kucoin')
        self._setUrl('https://api.kucoin.com/api/v1/')

    def _responseOk(self, response: requests.Response) -> bool:
        if response == None:
            return False

        if response.status_code == 200:
            # check for json response
            # check for return code of 20000 in json
            return True
        else:
            print('There was a problem sending the request ({:s}) ({:d}).'.format(response.url, response.status_code))
            return False

    def _getApiInfo(self):
        fstr = open('secrets.cfg', 'r').read()
        matches = re.findall(
                r'\s*<exchange\s*name=\"([a-zZ-z]+)\">\n\s*<api_key>([0-9a-f]+)</api_key>\n\s*<api_secret>([0-9a-f-]+)</api_secret>\n\s*<api_passphrase>(.*)</api_passphrase>\n\s*</exchange>',
                fstr
        )
        for match in matches:
            if match[0].lower() == self.getName().lower():
                # we have api info in the cfg file
                return match

        print('ERROR: API key for \'' + self.getName() + '\' exchange not found in secrets.cfg.')
        return None

    # private helper methods
    def _formatRequestHeaders(self, endpoint: str) -> dict:
        # move these keys to a kucoin config file
        apiInfo = self._getApiInfo()

        api_key = apiInfo[1]
        api_secret = apiInfo[2]
        api_passphrase = apiInfo[3]

        timestamp = int(time.time() * 1000)
        str_to_sign = str(timestamp) + 'GET' + '/api/v1/' + endpoint
        signature = base64.b64encode(hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
        passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
        headers = {
            'KC-API-SIGN': signature,
            'KC-API-TIMESTAMP': str(timestamp),
            'KC-API-KEY': api_key,
            'KC-API-PASSPHRASE': passphrase,
            'KC-API-KEY-VERSION': '2'
        }
        return headers

    # api methods
    def getSymbols(self) -> dict:
        endpoint = 'symbols'
        response = requests.get(self.getUrl() + endpoint)
        if not self._responseOk(response):
            return None

        return response.json()

    def getTime(self) -> dict:
        endpoint = 'timestamp'
        # this server reports UTC time
        time = {}
        response = requests.get(self.getUrl() + endpoint)
        if not self._responseOk(response):
            return None

        time['serverTime'] = response.json()['data']
        return time

    async def getSymbolInfo(self, symbol: str) -> dict:
        endpoint = 'market/orderbook/level1'
        param = '?symbol=' + symbol

        response = requests.get(self.getUrl() + endpoint + param)
        if not self._responseOk(response):
            return None

        return response.json()

    def getHistoricalData(self, symbol: str, interval: int, start: int, limit: int) -> dict:
        pass

    def getAccountInfo(self) -> dict:
        endpoint = 'accounts'
        headers = self._formatRequestHeaders(endpoint)
        if headers == None:
            return None
        response = requests.request('get', self.getUrl() + endpoint, headers=headers)
        if not self._responseOk(response):
            return None

        return response.json()

    def getMarginAccountInfo(self) -> dict:
        endpoint = 'margin/account'
        headers = self._formatRequestHeaders(endpoint)
        if headers == None:
            return None
        response = requests.request('get', self.getUrl() + endpoint, headers=headers)
        if not self._responseOk(response):
            return None

        return response.json()
