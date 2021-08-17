from data_streams import volumestream, tradingview
import json
import time
import threading

class TradeEngine:

    def __init__(self):
        self.monitoredCoins = {
            'BTCUSDT':{
                'exchange': 'KUCOIN',
                'last_price': None,
                'is_tradable': None,
                'volume': None
            },
            'ETHUSDT':{
                'exchange': 'KUCOIN',
                'last_price': None,
                'is_tradable': None,
                'volume': None
            }
        }
        self.symbols = self._constructSymbols()
        self.volumeStream = volumestream.VolumeStream(self.symbols)
        self.tv = tradingview.TradingView()

    def _constructSymbols(self):
        symbols = list(self.monitoredCoins.keys())
        for symbol in symbols:
            symbol = symbol.upper()

        exchanges = []
        for coin in list(self.monitoredCoins.values()):
            exchanges.append(coin['exchange'].upper())

        constructedSymbols = []
        for i in range(0, len(symbols)):
            constructedSymbols.append(f'{exchanges[i]}:{symbols[i]}')

        return constructedSymbols


    def on_volumeStream_receive(self, ws, message):
        if 'volume' in message:
            p = message.split('~', -1)[4]
            data = json.loads(p)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            symbol = data['p'][1]['n']
            volume = data['p'][1]['v']['volume']

            if symbol.upper() == symbol:
                print(f'tick :timestamp: {timestamp} :symbol: {symbol} :volume: {volume}')

def main():
    te = TradeEngine()

    volumeThread = threading.Thread(target=te.volumeStream.stream, args=(te.on_volumeStream_receive,))
    volumeThread.setDaemon(True) # set as background thread so it joins when main thread is done

    tvThread = threading.Thread(target=te.tv.pollSymbols, args=(te.symbols,))
    tvThread.setDaemon(True) # set as background thread so it joins when main thread is done

    print('starting data threads')
    volumeThread.start()
    tvThread.start()

    print('this is going on after the threads started')

    time.sleep(15)

if __name__ == '__main__':
    main()
