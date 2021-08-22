import requests
from enum import Enum

class ExchangeName(Enum):
    KUCOIN = 'Kucoin'
    BITRUE = 'Bitrue'
    BYBIT = 'Bybit'


class Exchange:

    def __init__(self):
        self._name = None
        self._url = None

    def __eq__(self, obj):
        if (type(obj) is type(self)):
            if (obj.get_name() == self.get_name()):
                if (obj.get_url() == self.get_url()):
                    return True
        return False

    def _response_ok(self, response: requests.Response) -> bool:
        if response == None:
            return False

        if response.status_code == 200:
            # check for json response
            # check for return code of 20000 in json
            return True
        else:
            print('There was a problem sending the request ({:s}) ({:d}).'.format(response.url, response.status_code))
            return False

    def set_url(self, url: str):
        self._url = url

    def set_name(self, name):
        if (type(name) != ExchangeName):
            raise TypeError('name must be of type \'ExchangeName\'')
        self._name = name

    def get_url(self) -> str:
        return self._url

    def get_name(self) -> ExchangeName:
        return self._name
