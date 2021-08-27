from exchanges.exchange import Exchange
from exchanges.exchange import ExchangeName

import hashlib
import hmac
import base64
import requests
import re
import time
import urllib3


class KucoinExchange(Exchange):

    def __init__(self):
        self.set_name(ExchangeName.KUCOIN)
        self.set_url('https://api.kucoin.com/api/v1/')

    def _get_api_info(self) -> dict:
        fstr = open('secrets.cfg', 'r').read()
        matches = re.findall(
                r'\s*<exchange\s*name=\"([a-zA-z]+)\">\n\s*<api_key>([0-9a-f]+)</api_key>\n\s*<api_secret>([0-9a-f-]+)</api_secret>\n\s*<api_passphrase>(.*)</api_passphrase>\n\s*</exchange>',
                fstr
        )
        for match in matches:
            if match[0] == self.get_name().value:
                # we have api info in the cfg file
                return {"success": match}

        print(f'ERROR: API key for \'{self.get_name()}\' exchange not found in secrets.cfg.')
        return {"error": f"API key for \'{self.get_name()}\' exchange not found in secrets.cfg."}

    # private helper methods
    def _format_request_headers(self, endpoint: str) -> dict:
        # move these keys to a kucoin config file
        api_info = self._get_api_info()
        if "error" in api_info:
            return api_info # returns error message dict

        print(api_info)
        api_key = api_info['success'][1]
        api_secret = api_info['success'][2]
        api_passphrase = api_info['success'][3]

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
        if "error" in headers:
            return headers # return error message

        try:
            response = requests.request('get', self.get_url() + endpoint, headers=headers)
            if not self._response_ok(response):
                return {"error": f"there was a problem with your request ({response.status_code})"}

            return response.json()
        except requests.exceptions.ConnectionError:
            print('Connection error')
            return {"error": "Could not connect to Kucoin exchange API"}

    def get_margin_account_info(self) -> dict:
        endpoint = 'margin/account'
        headers = self._format_request_headers(endpoint)
        if "error" in headers:
            return headers # return error message

        try:
            response = requests.request('get', self.get_url() + endpoint, headers=headers)
            if not self._response_ok(response):
                return {"error": f"there was a problem with your request ({response.status_code})"}

            return response.json()
        except requests.exceptions.ConnectionError:
            print("Connection error")
            return {"error": "Could not connect to Kucoin exchange API"}

        return response.json()
