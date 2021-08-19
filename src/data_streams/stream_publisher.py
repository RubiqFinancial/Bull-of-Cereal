from stream_subscriber import StreamSubscriber

class StreamPublisher:

    def __init__(self):
        self.name = None
        self._data = {'stream', self.name}
        self._subscribers = []
        pass

    def subscribe(self, subscriber: StreamSubscriber):
        pass

    def unsubscribe(self, subscriber: StreamSubscriber):
        pass

    def notify(self):
        pass
