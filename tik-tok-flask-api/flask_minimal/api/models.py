from flask_restful import Resource, Api, fields, abort
from flask import request
import json
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate(
    '/Users/rickywinarko/Documents/Github/TikTok/TIK-TOK-FLASK-API/credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


class DummyResult(Resource):
    def get(self):
        # ref = db.reference("/E-Wallet")
        # ref.set({
        #     "Books":
        #     {
        #         "Best_Sellers": -1
        #     }
        # })

        ref = db.document("users/z7zbK5xAnh9ORgj68Q4m")

        # with open("book_info.json", "r") as f:
        #     file_contents = json.load(f)

        # for key, value in file_contents.items():
        # ref.set({"dummy": "test"})
        return {"dummy": ref.get().to_dict()}


class HelloResult(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        name = json_data["name"]
        return {"greetings": "Hello {}".format(name)}
