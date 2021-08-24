from enum import Enum


class Interval(Enum):
    ONE_MINUTE = '1'
    FIFTEEN_MINUTE = '15'
    THIRTY_MINUTE = '30'
    ONE_HOUR = '60'
    TWO_HOUR = '120'
    ONE_DAY = '1D'


class Candle:

    def __init__(self, interval: Interval):
        self.interval = interval
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0

    def __eq__(self, obj) -> bool:
        if type(self) != type(obj):
            return False

        return (obj.interval == self.interval and
               obj.open == self.open and
               obj.high == self.high and
               obj.low == self.low and
               obj.close == self.close)

    def get_json(self) -> dict:
        return {
            'interval': self.interval,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
        }
