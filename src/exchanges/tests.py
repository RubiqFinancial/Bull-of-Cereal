from exchanges import bitruexc, kucoinxc, exchange, exchangemanager, exchangepool

import re
import time
import requests
import asyncio
import unittest

class TestExchangeMethods(unittest.TestCase):

    def test_Exchange(self):
        xc = exchange.Exchange()
        self.assertEqual(xc._name, None)
        self.assertEqual(xc._url, None)

    def test_set_name(self):
        xc = exchange.Exchange()
        xc.set_name(exchange.ExchangeName.BITRUE)
        self.assertEqual(type(xc._name), type(exchange.ExchangeName.BITRUE))
        self.assertEqual(xc._name.value, exchange.ExchangeName.BITRUE.value)

    def test_set_url(self):
        xc = exchange.Exchange()
        xc.set_url('bar.com')
        self.assertEqual(xc._url, 'bar.com')

    def test_get_name(self):
        xc = exchange.Exchange()
        xc.set_name(exchange.ExchangeName.KUCOIN)
        self.assertEqual(type(xc._name), type(exchange.ExchangeName.KUCOIN))
        self.assertEqual(xc._name.value, exchange.ExchangeName.KUCOIN.value)

    def test_get_name_exception(self):
        xc = exchange.Exchange()
        self.assertRaises(TypeError, xc.set_name, 'foo')

    def tesT_get_url(self):
        xc = exchange.Exchange()
        xc.set_url('bar.com')
        self.assertEqual(xc.get_name(), 'bar.com')

class TestExchangeManagerMethods(unittest.TestCase):

    def test_get_exchanges(self):
        xc_manager = exchangemanager.ExchangeManager()
        self.assertEqual(xc_manager.get_exchanges(), [kucoinxc.KucoinExchange(), bitruexc.BitrueExchange()])

    def test_get_exchange_bitrue(self):
        xc_manager = exchangemanager.ExchangeManager()
        self.assertEqual(xc_manager.get_exchange(exchange.ExchangeName.BITRUE), bitruexc.BitrueExchange())

    def test_get_exchange_kucoin(self):
        xc_manager = exchangemanager.ExchangeManager()
        self.assertEqual(xc_manager.get_exchange(exchange.ExchangeName.KUCOIN), kucoinxc.KucoinExchange())

if __name__ == '__main__':
    unittest.main()
