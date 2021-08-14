from exchanges import exchangepool
from exchanges import bitruexc
from exchanges import kucoinxc
from exchanges import exchange
# from utils import mycoroutine

import re
import time
import requests
import asyncio

async def main():
    exchangePool = exchangepool.ExchangePool({'kucoin': 0})
    exchangePool.addExchange('bitrue', bitruexc.BitrueExchange())
    exchangePool.addExchange('kucoin', kucoinxc.KucoinExchange())

if __name__ == '__main__':
    asyncio.run(main())
