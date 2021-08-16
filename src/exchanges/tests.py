import bitruexc, kucoinxc, exchange, exchangemanager, exchangepool

import re
import time
import requests
import asyncio
import unittest

class TestExchangeMethods(unittest.TestCase):

    def test_Exchange(self):
        xc = exchange.Exchange()
        with self.subTest():
            self.assertEqual(xc._namestr, None)
        with self.subTest():
            self.assertEqual(xc._url, None)

    def test_setName(self):
        xc = exchange.Exchange()
        xc.setName('foo')
        self.assertEqual(xc._namestr, 'foo')

    def test_setUrl(self):
        xc = exchange.Exchange()
        xc.setUrl('bar.com')
        self.assertEqual(xc._url, 'bar.com')

    def test_getName(self):
        xc = exchange.Exchange()
        xc.setName('foo')
        self.assertEqual(xc.getName(), 'foo')

    def tesT_getUrl(self):
        xc = exchange.Exchange()
        xc.setUrl('bar.com')
        self.assertEqual(xc.getName(), 'bar.com')

class TestExchangeManagerMethods(unittest.TestCase):

    def test_getExchanges(self):
        xcManager = exchangemanager.ExchangeManager()
        self.assertEqual(xcManager.getExchanges(), [kucoinxc.KucoinExchange(), bitruexc.BitrueExchange()])

    def test_getExchange_bitrue(self):
        xcManager = exchangemanager.ExchangeManager()
        self.assertEqual(xcManager.getExchange('bitrue'), bitruexc.BitrueExchange())

    def test_getExchange_kucoin(self):
        xcManager = exchangemanager.ExchangeManager()
        self.assertEqual(xcManager.getExchange('kucoin'), kucoinxc.KucoinExchange())

if __name__ == '__main__':
    unittest.main()
