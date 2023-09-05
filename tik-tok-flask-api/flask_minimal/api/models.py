from flask_restful import Resource, Api, fields, abort, reqparse
from flask import request
import json
import bcrypt

# FIREBASE DEP
import firebase_admin
from firebase_admin import credentials, firestore, db

# cred initialization - to comment out
cred = credentials.Certificate(
    '/Users/rickywinarko/Documents/GitHub/TikTok/tik-tok-flask-api/credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


class CreateUser(Resource):
    def post(self):
        try:
            user_data = request.get_json(force=True)
            email = user_data['email']
            name = user_data['name']
            phone = user_data['phone']
            pin = user_data['pin']
            currency = user_data['currency']

            # create salt for pwd hashing
            salt = bcrypt.gensalt()
            hashed_pin = bcrypt.hashpw(pin.encode('utf-8'), salt)

            user_ref = db.collection('users')
            phone_query = user_ref.where('phone', '==', phone).get()
            if phone_query:
                return {'error': 'Phone number already exists'}, 400

            email_query = user_ref.where('email', '==', email).get()
            if email_query:
                return {'error': 'Email Address already exists'}, 400

            user_ref.add({
                'email': email,
                'name': name,
                'phone': phone,
                # Store the hashed PIN as a string
                'hashed_pin': hashed_pin.decode('utf-8'),
                'salt': salt.decode('utf-8'),  # Store the salt as a string
                # initializing balance
                'balance': {item: 0 for item in currency},
                'transaction': []
            })
            return {'message': 'User registered successfully'}, 201
        except Exception as e:
            return {"error": f"error happened at creating user, {e}"}

# GET API to search for user document id


class SearchUser(Resource):
    def get(self):
        try:
            search_query = request.args.get('user')

            if not search_query:
                return {'error': 'Search query is required'}, 400

            user_ref = db.collection("users")
            query = user_ref.where('name', '==', search_query).stream()
            doc_ids = []

            # Iterate through the query results
            for doc in query:
                doc_ids.append(doc.id)

            if len(doc_ids) != 0:
                return {'results': doc_ids}
            else:
                return {'error': 'User not found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500

# maybe can add JWT and also take a look at security check/rule via firebase for double layer protection


class GetProfile(Resource):
    def get(self):
        try:
            phone = request.args.get('phone')
            pin = request.args.get('pin')

            if not (phone and pin):
                return {'error': 'Phone and Pin query are required'}, 400

            user_ref = db.collection("users")
            query = user_ref.where('phone', '==', phone).limit(1).stream()

            if not query:
                return {'error': 'Phone number does not exist'}, 400

            # Iterate through the query results
            for doc in query:
                user_data = doc.to_dict()
                hashed_pin = user_data.get('hashed_pin', '')

            if bcrypt.checkpw(pin.encode('utf-8'), hashed_pin.encode('utf-8')):
                # PIN matches, return user data without PIN and salt
                user_data.pop('hashed_pin', None)
                user_data.pop('salt', None)
                return {'message': 'PIN matches, data returned', 'user_data': user_data}, 201
            else:
                return {'error': 'Credentials not matched/found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500


class CreateTransaction(Resource):
    def post(self):
        try:
            transaction_parameters = request.get_json(force=True)
            sender = transaction_parameters['sender']
            receiver = transaction_parameters['receiver']
            amount = transaction_parameters['amount']
            currency = transaction_parameters['currency'].upper()

            users_ref = db.collection('users')
            sender_doc = users_ref.document(sender).get()
            receiver_doc = users_ref.document(receiver).get()

            if not sender_doc.exists or not receiver_doc.exists:
                return {'error': 'Sender or receiver does not exist'}, 404

            if not (currency in sender_doc.get("balance") and currency in receiver_doc.get("balance")):
                return {'error': 'Sender or receiver does not have the currency selected'}, 404

            sender_transactions_ref = db.collection('transactions')
            sender_transactions_ref.add({
                'receiver_user_id': sender,
                'sender_user_id': receiver,
                'amount': amount,  # Debit amount is negative
                'type': 'credit'
            })

            receiver_transactions_ref = db.collection('transactions')
            receiver_transactions_ref.add({
                'receiver_user_id': receiver,
                'sender_user_id': receiver,
                'amount': amount,  # Debit amount is negative
                'type': 'credit'
            })

            # Update user balances using double-entry accounting
            sender_balance = sender_doc.get('balance').get(currency)
            receiver_balance = receiver_doc.get('balance').get(currency)

            # if (sender_balance - amount)

            sender_doc.reference.update(
                {'balance.' + currency: sender_balance - amount})

            # Credit receiver's account
            receiver_doc.reference.update(
                {'balance.' + currency: receiver_balance + amount})

            return {'message': 'Transfer transaction created successfully'}, 201
        except Exception as e:
            return {"error": f"error happened at: {e}"}
