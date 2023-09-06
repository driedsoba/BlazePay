from flask_restful import Resource, Api, fields, abort, reqparse
from flask import request
import json
import bcrypt
import uuid

# FIREBASE DEP
import firebase_admin
from firebase_admin import credentials, firestore, db

# cred initialization - to comment out
cred = credentials.Certificate('../tik-tok-flask-api/credentials.json')
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
                'hashed_pin': hashed_pin.decode('utf-8'),
                'salt': salt.decode('utf-8'),
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
                user_id = doc.id
                hashed_pin = user_data.get('hashed_pin', '')

            if bcrypt.checkpw(pin.encode('utf-8'), hashed_pin.encode('utf-8')):
                # PIN matches, return user data without PIN and salt
                user_data.pop('hashed_pin', None)
                user_data.pop('salt', None)
                return {'message': 'PIN matches, data returned', 'user_data': user_data, 'user_id': user_id}, 201
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
            transaction_id = str(uuid.uuid4())

            users_ref = db.collection('users')
            sender_doc = users_ref.document(sender).get()
            receiver_doc = users_ref.document(receiver).get()

            if not sender_doc.exists or not receiver_doc.exists:
                return {'error': 'Sender or receiver does not exist'}, 404

            if not (currency in sender_doc.get("balance") and currency in receiver_doc.get("balance")):
                return {'error': 'Sender or receiver does not have the currency selected'}, 404

            sender_transactions_ref = db.collection('transactions').document(sender+'-'+transaction_id)
            sender_transactions_ref.set({
                'transaction_acc': sender,
                'receiver_user_id': sender,
                'sender_user_id': receiver,
                'amount': -amount,  # Debit amount is negative
                'currency': currency,
                'type': 'credit'
            })

            receiver_transactions_ref = db.collection('transactions').document(receiver+'-'+transaction_id)
            receiver_transactions_ref.set({
                'transaction_acc': receiver,
                'receiver_user_id': sender,
                'sender_user_id': receiver,
                'amount': amount,  # Debit amount is negative
                'currency': currency,
                'type': 'debit'
            })

            prefix_to_search =[sender, receiver]
            total_balance={}
            for prefix in prefix_to_search:
                print(prefix)
                query = db.collection('transactions').where("transaction_acc", "==", prefix )
                total_amount = 0
                # Execute the query to retrieve matching documents
                docs = query.stream()
                # Iterate through the matching documents and access their "amount" field
                for doc in docs:
                    data = doc.to_dict()
                    print(data)
                    if "amount" in data and data['currency']==currency:
                        amount = data["amount"]
                        total_amount += amount

                total_balance[prefix]= total_amount

            # Update user balances using double-entry accounting
            sender_balance = sender_doc.get('balance').get(currency)
            receiver_balance = receiver_doc.get('balance').get(currency)

            if total_balance[sender]==sender_balance-amount:
                sender_doc.reference.update({'balance.' + currency: sender_balance - amount})

            if total_balance[receiver]==receiver_balance+amount:
                receiver_doc.reference.update({'balance.' + currency: receiver_balance + amount})

            return {'message': 'Transfer transaction created successfully'}, 201
        except Exception as e:
            return {"error": f"error happened at: {e}"}
