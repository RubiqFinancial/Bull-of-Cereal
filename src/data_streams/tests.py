from data_streams import autoview
from trade_engine import engine

import unittest


class TestAutoview(unittest.TestCase):

    def test_init_autoview(self):
        av = autoview.Autoview()
        self.assertEqual(av.name, 'Autoview')
        self.assertEqual(av._data, {'stream': 'Autoview'})
        self.assertEqual(av._subscribers, [])

    def test_add_subscriber(self):
        av = autoview.Autoview()
        subscriber = engine.TradeEngine()
        av.add_subscriber(subscriber)
        self.assertEqual(av._subscribers, [subscriber])

    def test_remove_subscriber(self):
        av = autoview.Autoview()
        subscriber = engine.TradeEngine()
        av.add_subscriber(subscriber)
        self.assertEqual(av._subscribers, [subscriber])
        av.remove_subscriber(subscriber)
        self.assertEqual(av._subscribers, [])

    def test_notify(self):
        pass

    def test_set_data(self):
        pass


if __name__ == '__main__':
    unittest.main()
