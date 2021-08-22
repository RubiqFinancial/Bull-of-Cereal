from trade_engine import engine, coin, candle
from exchanges import exchange
import tradingview_ta as tv
import unittest

class TestTradeEngine(unittest.TestCase):
    pass

class TestCoin(unittest.TestCase):

    def test_coin_init_params(self):
        test_coin = coin.Coin(coin.Currency.BTC, coin.Currency.USDT, exchange.ExchangeName.KUCOIN)
        self.assertEqual(test_coin.base, coin.Currency.BTC)
        self.assertEqual(test_coin.quote, coin.Currency.USDT)
        self.assertEqual(test_coin.exchange, exchange.ExchangeName.KUCOIN)

    def test_coin_init_price(self):
        test_coin = coin.Coin(coin.Currency.BTC, coin.Currency.USDT, exchange.ExchangeName.KUCOIN)
        self.assertEqual(test_coin.price, 0.0)

    def test_coin_init_vol(self):
        test_coin = coin.Coin(coin.Currency.BTC, coin.Currency.USDT, exchange.ExchangeName.KUCOIN)
        self.assertEqual(test_coin.volume, 0.0)

    def test_coin_init_chp(self):
        test_coin = coin.Coin(coin.Currency.BTC, coin.Currency.USDT, exchange.ExchangeName.KUCOIN)
        self.assertEqual(test_coin.price_change, 0.0)

    def test_coin_init_chv(self):
        test_coin = coin.Coin(coin.Currency.BTC, coin.Currency.USDT, exchange.ExchangeName.KUCOIN)
        self.assertEqual(test_coin.volume_change, 0.0)

    def test_coin_init_rating(self):
        test_coin = coin.Coin(coin.Currency.BTC, coin.Currency.USDT, exchange.ExchangeName.KUCOIN)
        self.assertEqual(test_coin.rating, None)

    def test_coin_init_candles(self):
        test_coin = coin.Coin(coin.Currency.BTC, coin.Currency.USDT, exchange.ExchangeName.KUCOIN)
        self.assertEqual(test_coin.candles, {
                candle.Interval.ONE_MINUTE: candle.Candle(candle.Interval.ONE_MINUTE),
                candle.Interval.FIFTEEN_MINUTE: candle.Candle(candle.Interval.FIFTEEN_MINUTE),
                candle.Interval.ONE_HOUR: candle.Candle(candle.Interval.ONE_HOUR)
        })

    def test_coin_init_emas(self):
        test_coin = coin.Coin(coin.Currency.BTC, coin.Currency.USDT, exchange.ExchangeName.KUCOIN)
        self.assertEqual(test_coin.ema5, 0.0)
        self.assertEqual(test_coin.ema13, 0.0)
        self.assertEqual(test_coin.ema50, 0.0)
        self.assertEqual(test_coin.ema200, 0.0)
        self.assertEqual(test_coin.ema800, 0.0)

    def test_coin_get_json(self):
        test_coin = coin.Coin(coin.Currency.BTC, coin.Currency.USDT, exchange.ExchangeName.KUCOIN)
        keys = ['base', 'quote', 'exchange', 'price', 'volume', 'priceChange', 'volumeChange',
                'rating', 'candles', 'ema5', 'ema13', 'ema50', 'ema200', 'ema800']
        self.assertEqual(list(test_coin.get_json()), keys)

    def test_coin_get_symbol_string(self):
        test_coin = coin.Coin(coin.Currency.BTC, coin.Currency.USDT, exchange.ExchangeName.KUCOIN)
        self.assertEqual(test_coin.get_symbol_string(), 'BTC:USDT')

class TestCandles(unittest.TestCase):

    def test_candle_interval(self):
        self.assertEqual(candle.Interval.ONE_MINUTE.value, '1')
        self.assertEqual(candle.Interval.FIFTEEN_MINUTE.value, '15')
        self.assertEqual(candle.Interval.THIRTY_MINUTE.value, '30')
        self.assertEqual(candle.Interval.ONE_HOUR.value, '60')
        self.assertEqual(candle.Interval.TWO_HOUR.value, '120')
        self.assertEqual(candle.Interval.ONE_DAY.value, '1D')

    def test_candle_init_1(self):
        test_candle = candle.Candle(candle.Interval.ONE_MINUTE)
        self.assertEqual(test_candle.interval, candle.Interval.ONE_MINUTE)

    def test_candle_init_15(self):
        test_candle = candle.Candle(candle.Interval.FIFTEEN_MINUTE)
        self.assertEqual(test_candle.interval, candle.Interval.FIFTEEN_MINUTE)

    def test_candle_init_30(self):
        test_candle = candle.Candle(candle.Interval.THIRTY_MINUTE)
        self.assertEqual(test_candle.interval, candle.Interval.THIRTY_MINUTE)

    def test_candle_init_60(self):
        test_candle = candle.Candle(candle.Interval.ONE_HOUR)
        self.assertEqual(test_candle.interval, candle.Interval.ONE_HOUR)

    def test_candle_init_120(self):
        test_candle = candle.Candle(candle.Interval.TWO_HOUR)
        self.assertEqual(test_candle.interval, candle.Interval.TWO_HOUR)

    def test_candle_init_1D(self):
        test_candle = candle.Candle(candle.Interval.ONE_DAY)
        self.assertEqual(test_candle.interval, candle.Interval.ONE_DAY)

    def test_candle_get_json(self):
        test_candle = candle.Candle(candle.Interval.ONE_MINUTE)
        keys = ['interval', 'open', 'high', 'low', 'close']
        self.assertEqual(list(test_candle.get_json()), keys)
        self.assertEqual(test_candle.get_json()['interval'], candle.Interval.ONE_MINUTE)

if __name__ == '__main__':
    unittest.main()
