from flask import Flask
import exchangemanager
import asyncio

app = Flask(__name__)
xcManager = exchangemanager.ExchangeManager()

@app.route('/api/')
def index():
    return 'Bull of Cereal private API home'

@app.route('/api/exchanges')
async def getExchanges() -> dict:
    exchanges = xcManager.getExchanges()

    rjson = {}
    coroutines = []

    for exchange in exchanges:
        coroutines.append(exchange.getTime())

    result = await asyncio.gather(*coroutines)

    for i in range(0, len(exchanges)):
        rjson[exchanges[i].getName()] = result[i]

    return rjson

@app.route('/api/exchanges/trade')
async def makeTrade() -> dict:
    return 'this endpoint should be used to trade'

if __name__ == '__main__':
    asyncio.run(app.run(debug=True))
