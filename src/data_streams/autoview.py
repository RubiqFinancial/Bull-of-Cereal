from data_streams import stream_publisher as sp
from data_streams import stream_subscriber as ss

class AutoView(sp.StreamPublisher):

    def __init__(self):
        super().__init__()
        self.name = 'AutoView'
        self._data = {'stream': self.name}

    def subscribe(self, subscriber: ss.StreamSubscriber):
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: ss.StreamSubscriber):
        self._subscribers.remove(subscriber)

    def notify(self):
        for subscriber in self._subscribers:
            subscriber.update(self._data) # implement update as a new thread

    def setData(self, newData: dict):
        newKeys = list(newData)
        for key in newKeys:
            self._data[key] = newData[key]

        self.notify()
