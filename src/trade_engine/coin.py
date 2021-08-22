from trade_engine import candle
from exchanges import exchange
from enum import Enum

class Currency(Enum):
    USDT = 'USDT'
    BTC = 'BTC'
    ETH = 'ETH'
    LUNA = 'LUNA'
    BNB = 'BNB'
    ADA = 'ADA'
    DOGE = 'DOGE'


class Coin:

    # emas per candle
    def __init__(self, base: Currency, quote: Currency, exchange: exchange.ExchangeName):
        self.base = base
        self.quote = quote
        self.exchange = exchange
        self.price = 0.0
        self.volume = 0.0
        self.price_change = 0.0
        self.volume_change = 0.0
        self.rating = None
        self.candles = {
                candle.Interval.ONE_MINUTE: candle.Candle(candle.Interval.ONE_MINUTE),
                candle.Interval.FIFTEEN_MINUTE: candle.Candle(candle.Interval.FIFTEEN_MINUTE),
                candle.Interval.ONE_HOUR: candle.Candle(candle.Interval.ONE_HOUR)
        }
        self.ema5 = 0.0
        self.ema13 = 0.0
        self.ema50 = 0.0
        self.ema200 = 0.0
        self.ema800 = 0.0

    def __str__(self):
        return f'{self.get_json()}'

    def get_json(self) -> dict:
        return {
            'base': self.base,
            'quote': self.quote,
            'exchange': self.exchange,
            'price': self.price,
            'volume': self.volume,
            'priceChange': self.price_change,
            'volumeChange': self.volume_change,
            'rating': self.rating,
            'candles': {
                candle.Interval.ONE_MINUTE: self.candles[candle.Interval.ONE_MINUTE].get_json(),
                candle.Interval.FIFTEEN_MINUTE: self.candles[candle.Interval.FIFTEEN_MINUTE].get_json(),
                candle.Interval.ONE_HOUR: self.candles[candle.Interval.ONE_HOUR].get_json()
            },
            'ema5': self.ema5,
            'ema13': self.ema13,
            'ema50': self.ema50,
            'ema200': self.ema200,
            'ema800': self.ema800
        }

    def get_symbol_string(self) -> str:
        return f'{self.exchange.value}:{self.base.value}{self.quote.value}'
