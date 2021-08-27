import requests
from exchanges import exchangemanager
from trade_engine import engine


def main():
    base = 'http://127.0.0.1:5000/api/'
    endpoint = 'engine'
    # response = requests.post('http://localhost:5000/api/alerts', {'msg': 'hello world'})
    # print(response.json())
    url = f'{base}{endpoint}'
    te = engine.TradeEngine()
    coin_json_list = [coin.get_symbol_string() for coin in te.monitored_coins]
    print(coin_json_list)
    # response = requests.post(url, {'coins', coin_json_list})
    # print(response.json())


if __name__ == '__main__':
    main()
