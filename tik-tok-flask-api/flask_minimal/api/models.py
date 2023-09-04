from flask_restful import Resource, Api, fields, abort
from flask import request


class DummyResult(Resource):
    def get(self):
        return {"dummy": "test"}


class HelloResult(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        name = json_data["name"]
        return {"greetings": "Hello {}".format(name)}
