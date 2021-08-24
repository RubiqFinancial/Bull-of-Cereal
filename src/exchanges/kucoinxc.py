from exchanges.exchange import Exchange
from exchanges.exchange import ExchangeName

import hashlib
import hmac
import base64
import requests
import re
import time


class KucoinExchange(Exchange):

    def __init__(self):
        self.set_name(ExchangeName.KUCOIN)
        self.set_url('https://api.kucoin.com/api/v1/')

    def _get_api_info(self):
        fstr = open('secrets.cfg', 'r').read()
        matches = re.findall(
                r'\s*<exchange\s*name=\"([a-zZ-z]+)\">\n\s*<api_key>([0-9a-f]+)</api_key>\n\s*<api_secret>([0-9a-f-]+)</api_secret>\n\s*<api_passphrase>(.*)</api_passphrase>\n\s*</exchange>',
                fstr
        )
        for match in matches:
            if match[0].lower() == self.get_name().lower():
                # we have api info in the cfg file
                return match

        print('ERROR: API key for \'' + self.get_name() + '\' exchange not found in secrets.cfg.')
        return None

    # private helper methods
    def _format_request_headers(self, endpoint: str) -> dict:
        # move these keys to a kucoin config file
        api_info = self._get_api_info()

        api_key = api_info[1]
        api_secret = api_info[2]
        api_passphrase = api_info[3]

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
    def get_symbols(self) -> dict:
        endpoint = 'symbols'
        response = requests.get(self.get_url() + endpoint)
        if not self._response_ok(response):
            return None

        return response.json()

    async def get_time(self) -> dict:
        endpoint = 'timestamp'
        # this server reports UTC time
        xc_time = {}
        response = requests.get(self.get_url() + endpoint)
        if not self._response_ok(response):
            return None

        xc_time['serverTime'] = response.json()['data']
        return xc_time

    def get_symbol_info(self, symbol: str) -> dict:
        endpoint = 'market/orderbook/level1'
        param = '?symbol=' + symbol

        response = requests.get(self.get_url() + endpoint + param)
        if not self._response_ok(response):
            return None

        return response.json()

    def get_historical_data(self, symbol: str, interval: int, start: int, limit: int) -> dict:
        pass

    def get_account_info(self) -> dict:
        endpoint = 'accounts'
        headers = self._format_request_headers(endpoint)
        if headers is None:
            return None
        response = requests.request('get', self.get_url() + endpoint, headers=headers)
        if not self._response_ok(response):
            return None

        return response.json()

    def get_margin_account_info(self) -> dict:
        endpoint = 'margin/account'
        headers = self._format_request_headers(endpoint)
        if headers is None:
            return None
        response = requests.request('get', self.get_url() + endpoint, headers=headers)
        if not self._response_ok(response):
            return None

        return response.json()
