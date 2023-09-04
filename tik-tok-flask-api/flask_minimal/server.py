from flask import Flask, request
from flask_restful import Api, Resource
from flask_minimal.api.models import *

app = Flask(__name__)
api = Api(app)

api.add_resource(DummyResult, '/dummy')
api.add_resource(CreateTransaction, '/hello')

def run_app(*args, **kwargs):
    app.run(*args, **kwargs, port=3000)

if __name__ == '__main__':
    app.run(debug=True)
