from data_streams import tradingview_websocket
import asyncio

class VolumeStream:

    def __init__(self, symbols):
        self.symbols = symbols
        self.fields = ['volume']
        self.tvws = tradingview_websocket.TradingViewWebSocket(self.symbols, self.fields)

    def stream(self, on_message):
        ws = self.tvws.createWebSocket(on_message=on_message)
        ws.run_forever()
