from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Bull of Cereal private API home'

@app.route('/exchanges')
def getExchanges():
    return {'Kucoin': 'exchange json', 'Bitrue': 'exchange json'}

if __name__ == '__main__':
    app.run(debug=True)
