class Exchange:

    def __init__(self):
        self._namestr = None
        self._url = None

    def __eq__(self, obj):
        if (type(obj) is type(self)):
            if (obj.getName() == self.getName()):
                if (obj.getUrl() == self.getUrl()):
                    return True
        return False

    def setUrl(self, url):
        self._url = url

    def setName(self, name):
        self._namestr = name

    def getUrl(self):
        return self._url

    def getName(self):
        return self._namestr
