from exchanges.exchange import Exchange
from exchanges.exchange import ExchangeName

import requests


class BitrueExchange(Exchange):

    def __init__(self):
        self.set_name(ExchangeName.BITRUE)
        self.set_url('https://www.bitrue.com/api/v1/')

    def get_symbols(self) -> dict:
        pass

    async def get_time(self) -> dict:
        endpoint = 'time'
        # this server reports UTC time
        response = requests.get(self.get_url() + endpoint)
        if not self._response_ok(response):
            return None

        return response.json()

    def get_symbol_price(self, symbol) -> dict:
        pass

    def get_historical_data(self, symbol, interval, start, limit) -> dict:
        pass

    def get_account_info(self) -> dict:
        pass

    def get_margin_account_info(self):
        print('error: bitrue cannot trade on margin')
