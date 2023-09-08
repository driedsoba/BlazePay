from flask import Flask, request
from flask_restful import Api, Resource
from flask_minimal.api.group_transaction import *
from flask_minimal.api.p2p_transaction import *
from flask_minimal.api.personal_transaction import *

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

app = Flask(__name__)
api = Api(app)

app.config['JWT_SECRET_KEY'] = 'ewallet123lesgo' 
jwt = JWTManager(app)

api.add_resource(SearchUser, '/searchID')
api.add_resource(GetProfile, '/profile')
api.add_resource(CreateTransaction, '/payment')
api.add_resource(CreateUser, '/newUser')
api.add_resource(TopUp, '/topUp')
api.add_resource(CreateGroupTransaction,'/group')
api.add_resource(CheckGroupTransaction,'/group/check')
api.add_resource(ProcessGroupPayment,'/group/payment')
api.add_resource(CreateStripePayment, '/stripe')
api.add_resource(stripe_webhook, '/webhook')

def run_app(*args, **kwargs):
    app.run(*args, **kwargs, port=3000)

if __name__ == '__main__':
    app.run(debug=True)
