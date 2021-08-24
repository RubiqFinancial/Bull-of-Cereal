from abc import abstractmethod


class StreamSubscriber:

    def __init__(self):
        pass

    @abstractmethod
    def update(self, data: dict):
        pass
