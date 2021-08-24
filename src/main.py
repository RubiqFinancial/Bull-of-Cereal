import requests
from exchanges import exchangemanager


def main():
    response = requests.post('http://localhost:5000/api/alerts', {'msg': 'hello world'})
    print(response.json())


if __name__ == '__main__':
    main()
