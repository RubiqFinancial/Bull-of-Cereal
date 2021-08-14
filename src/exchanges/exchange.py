class Exchange:

    def __init__(self):
        self._namestr = None
        self._url = None

    def setUrl(self, url):
        self._url = url

    def setName(self, name):
        self._namestr = name

    def getUrl(self):
        return self._url

    def getName(self):
        return self._namestr
