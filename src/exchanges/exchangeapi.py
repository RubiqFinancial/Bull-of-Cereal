from flask import Flask
from flask_restful import Resource, Api, reqparse
from exchanges import exchangemanager
import pandas as pd

app = Flask(__name__)
api = Api(app)


class Exchanges(Resource):
    def get(self):
        return {'exchange_name': 'exchange'}, 200


class Alerts(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('msg', required=False, type=str)
        args = parser.parse_args()
        print(args)

        return {'r': 'ack'}, 200


api.add_resource(Exchanges, '/api/exchanges')
api.add_resource(Alerts, '/api/alerts')

if __name__ == '__main__':
    app.run(debug=True)
