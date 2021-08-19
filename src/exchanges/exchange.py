class Exchange:

    KUCOIN = 'Kucoin'
    BITRUE = 'Bitrue'
    BYBIT = 'Bybit'

    def __init__(self):
        self._namestr = None
        self._url = None

    def __eq__(self, obj):
        if (type(obj) is type(self)):
            if (obj.getName() == self.getName()):
                if (obj.getUrl() == self.getUrl()):
                    return True
        return False

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

    def setUrl(self, url):
        self._url = url

    def setName(self, name):
        self._namestr = name

    def getUrl(self):
        return self._url

    def getName(self):
        return self._namestr
