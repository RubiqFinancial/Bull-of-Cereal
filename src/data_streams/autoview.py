from stream_publisher import StreamPublisher
from stream_subscriber import StreamSubscriber

class AutoView(StreamPublisher):

    def __init__(self):
        super().__init__()
        self.name = 'AutoView'
        self._data = {'stream': self.name}

    def subscribe(self, subscriber: StreamSubscriber):
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: StreamSubscriber):
        self._subscribers.remove(subscriber)

    def notify(self):
        for subscriber in self._subscribers:
            subscriber.update(self._data) # implement update as a new thread

    def setData(self, newData: dict):
        newKeys = list(newData)
        for key in newKeys:
            self._data[key] = newData[key]

        self.notify()
