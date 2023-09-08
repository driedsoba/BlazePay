from flask import Flask, request
from flask_restful import Api, Resource
from flask_minimal.api.models import *

app = Flask(__name__)
api = Api(app)

api.add_resource(SearchUser, '/searchID')
api.add_resource(GetProfile, '/profile')
api.add_resource(CreateTransaction, '/payment')
api.add_resource(CreateUser, '/newUser')
api.add_resource(TopUp, '/topUp')
api.add_resource(CreateStripePayment, '/stripe')
api.add_resource(stripe_webhook, '/webhook')


def run_app(*args, **kwargs):
    app.run(*args, **kwargs, port=3000)


if __name__ == '__main__':
    app.run(debug=True)
