from data_streams import stream_publisher as sp
from data_streams import stream_subscriber as ss
import threading


class Autoview(sp.StreamPublisher):

    def __init__(self):
        super().__init__()
        self.name = 'Autoview'
        self._data = {'stream': self.name}

    def add_subscriber(self, subscriber: ss.StreamSubscriber):
        self._subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: ss.StreamSubscriber):
        self._subscribers.remove(subscriber)

    def notify(self):
        for subscriber in self._subscribers:
            subscriber.update(self._data)

    # must invoke as daemon thread
    def set_data(self, new_data: dict):
        new_keys = list(new_data)
        for key in new_keys:
            self._data[key] = new_data[key]

        self.notify()
