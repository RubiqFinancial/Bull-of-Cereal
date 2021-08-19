class Candle:

    def __init__(self, interval: str):
        self.interval = None
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0


class Interval:

    ONE_MINUTE = '1m'
    FIFTEEN_MINUTE = '15m'
    ONE_HOUR = '1h'