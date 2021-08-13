from exchanges import exchangepool
from exchanges import bitruexc
from exchanges import kucoinxc

import re
import time
import requests

def main():
    exchangePool = exchangepool.ExchangePool({'kucoin': 0})
    exchangePool.add_exchange('bitrue', bitruexc.BitrueExchange())
    exchangePool.add_exchange('kucoin', kucoinxc.KucoinExchange())

    response = exchangePool.get_exchanges()['kucoin'].getSymbolInfo('BNB-BTC')
    print(response)


if __name__ == '__main__':
    main()
