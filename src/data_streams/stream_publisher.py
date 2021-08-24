from data_streams import stream_subscriber as ss
from abc import abstractmethod


class StreamPublisher:

    def __init__(self):
        self.name = None
        self._data = {'stream', self.name}
        self._subscribers = []
        pass

    @abstractmethod
    def add_subscriber(self, subscriber: ss.StreamSubscriber):
        pass

    @abstractmethod
    def remove_subscriber(self, subscriber: ss.StreamSubscriber):
        pass

    @abstractmethod
    def notify(self):
        pass

    @abstractmethod
    def set_data(self, data: dict):
        pass
