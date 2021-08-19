from trade_engine import candle

class Coin:

    # emas per candle
    def __init__(self, base: str, quote: str, exchange: str):
        self.base = base.upper()
        self.quote = quote.upper()
        self.exchange = exchange.upper()
        self.price = 0.0
        self.volume = 0.0
        self.priceChange = 0.0
        self.volumeChange = 0.0
        self.rating = None
        self.candles = [
                candle.Candle(candle.Interval.ONE_MINUTE),
                candle.Candle(candle.Interval.FIFTEEN_MINUTE),
                candle.Candle(candle.Interval.ONE_HOUR)
        ]
        self.ema5 = 0.0
        self.ema13 = 0.0
        self.ema50 = 0.0
        self.ema200 = 0.0
        self.ema800 = 0.0

    def __str__(self):
        return f'{self.getJson()}'

    def getJson(self) -> dict:
        pass

if __name__ == '__main__':
    coin = Coin('btc', 'usdt', 'kucoin')
