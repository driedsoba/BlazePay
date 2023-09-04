from flask import Flask, request
from flask_restful import Api, Resource
from flask_minimal.api.models import DummyResult
from flask_minimal.api.models import HelloResult

app = Flask(__name__)
api = Api(app)

api.add_resource(DummyResult, '/dummy')
api.add_resource(HelloResult, '/hello')


def run_app(*args, **kwargs):
    app.run(*args, **kwargs)


if __name__ == '__main__':
    app.run(debug=True)
