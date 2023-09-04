from flask_restful import Resource, Api, fields, abort, reqparse
from flask import request
import json
import firebase_admin
from firebase_admin import credentials, firestore, db

## cred initialization
cred = credentials.Certificate(
    '/Users/victorlim/Documents/projects/TikTok/tik-tok-flask-api/credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

## request parser for new endpoint
transaction_parser = reqparse.RequestParser()
transaction_parser.add_argument('sender', type=str, required=True, help='Sender is required')
transaction_parser.add_argument('receiver', type=str, required=True, help='Receiver is required')
transaction_parser.add_argument('amount', type=float, required=True, help='Amount is required')

class DummyResult(Resource):
    def get(self):
        users_ref = db.collection("users")
        users = users_ref.stream()
        for user in users:
            print(f"Document ID: {user.id}")
            print(f"Data: {user.to_dict()}")
        return {"dummy": "mee"}

class HelloResult(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        name = json_data["name"]
        return {"greetings": "Hello {}".format(name)}

class CreateTransaction(Resource):
    def post(self):
        try:
            args = transaction_parser.parse_args()
            sender = args['sender']
            receiver = args['receiver']
            amount = args['amount']

            users_ref = db.collection('users')
            sender_doc = users_ref.document(sender).get()
            receiver_doc = users_ref.document(receiver).get()

            if not sender_doc.exists or not receiver_doc.exists:
                return {'error': 'Sender or receiver does not exist'}, 404
            
            sender_transactions_ref = db.collection('transactions')
            sender_transaction_ref = sender_transactions_ref.add({
                'receiver_user_id': sender,
                'sender_user_id': receiver,
                'amount': -amount,  # Debit amount is negative
                'type': 'debit' 
            })
            
            receiver_transactions_ref = db.collection('transactions')
            receiver_transaction_ref = receiver_transactions_ref.add({
                'receiver_user_id': receiver,
                'sender_user_id': receiver,
                'amount': amount,  # Debit amount is negative
                'type': 'debit' 
            })

            # Update user balances using double-entry accounting
            sender_balance = sender_doc.get('balance')
            receiver_balance = receiver_doc.get('balance')

            sender_doc.reference.update({'balance': sender_balance - amount})

            # Credit receiver's account
            receiver_doc.reference.update({'balance': receiver_balance + amount})

            return {'message': 'Transfer transaction created successfully'}, 201
        except Exception as e:
            return {"error": f"error happened at: {e}"}

