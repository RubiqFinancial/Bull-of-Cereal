import engine
import tradingview_ta as tv
import unittest

class TestTradeEngine(unittest.TestCase):

    def test_querySymbol(self):
        tradeEngine = engine.TradeEngine()
        analysis = tradeEngine.querySymbol('ADAUSDT')
        self.assertEqual((type(analysis) == tv.main.Analysis), True)

if __name__ == '__main__':
    unittest.main()
