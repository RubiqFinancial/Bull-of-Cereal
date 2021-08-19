from data_streams import stream_subscriber as ss

class StreamPublisher:

    def __init__(self):
        self.name = None
        self._data = {'stream', self.name}
        self._subscribers = []
        pass

    def subscribe(self, subscriber: ss.StreamSubscriber):
        pass

    def unsubscribe(self, subscriber: ss.StreamSubscriber):
        pass

    def notify(self):
        pass
