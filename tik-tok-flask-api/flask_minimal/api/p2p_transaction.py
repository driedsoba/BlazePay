from flask_restful import Resource, Api, fields, abort, reqparse
from flask import request
import json
import bcrypt
import uuid
import stripe

# FIREBASE DEP
import firebase_admin
from firebase_admin import credentials, firestore, db
from flask_minimal.helpers import jwt_required_custom, SearchUser
from flask_jwt_extended import create_access_token, get_jwt_identity

# cred initialization - to comment out
from flask_minimal.firebase import db


class CreateTransaction(Resource):
    @jwt_required_custom
    def post(self):
        try:
            current_user = get_jwt_identity()
            transaction_parameters = request.get_json(force=True)
            sender = current_user
            receiver = SearchUser(transaction_parameters['receiver'])
            print(receiver)
            amount = transaction_parameters['amount']
            currency = transaction_parameters['currency'].upper()
            transaction_id = str(uuid.uuid4())

            users_ref = db.collection('users')
            sender_doc = users_ref.document(sender).get()
            receiver_doc = users_ref.document(receiver).get()

            if sender == receiver:
                return {'error': 'You cannot send money to yourself'}, 404

            if not sender_doc.exists or not receiver_doc.exists:
                return {'error': 'Sender or receiver does not exist'}, 404

            if not (currency in sender_doc.get("balance") and currency in receiver_doc.get("balance")):
                return {'error': 'Sender or receiver does not have the currency selected'}, 404

            # check whether the sender has enough money:
            if sender_doc.get('balance').get(currency) < amount:
                return {'error': 'You dont have enough money, please top up'}, 404
            else:
                pass

            sender_transactions_ref = db.collection(
                'transactions').document(sender+'-'+transaction_id)
            sender_transactions_ref.set({
                'transaction_acc': sender,
                'receiver_user_id': sender,
                'sender_user_id': receiver,
                'amount': -amount,  # Debit amount is negative
                'currency': currency,
                'type': 'credit',
                'mode': 'P2P',
                'status': False
            })

            receiver_transactions_ref = db.collection(
                'transactions').document(receiver+'-'+transaction_id)
            receiver_transactions_ref.set({
                'transaction_acc': receiver,
                'receiver_user_id': sender,
                'sender_user_id': receiver,
                'amount': amount,  # Debit amount is negative
                'currency': currency,
                'type': 'debit',
                'mode': 'P2P',
                'status': False
            })

            prefix_to_search = [sender, receiver]
            total_balance = {}
            for prefix in prefix_to_search:
                query = db.collection('transactions').where(
                    "transaction_acc", "==", prefix)
                total_amount = 0
                # Execute the query to retrieve matching documents
                docs = query.stream()
                # Iterate through the matching documents and access their "amount" field
                for doc in docs:
                    data = doc.to_dict()
                    if "amount" in data and data['currency'] == currency:
                        amount = data["amount"]
                        total_amount += amount

                total_balance[prefix] = total_amount
                print(total_balance)

            # Update user balances using double-entry accounting
            sender_balance = sender_doc.get('balance').get(currency)
            receiver_balance = receiver_doc.get('balance').get(currency)

            if total_balance[sender] == sender_balance-amount:
                sender_doc.reference.update(
                    {'balance.' + currency: sender_balance - amount})
                sender_transactions_ref.update({"status": True})

            if total_balance[receiver] == receiver_balance+amount:
                receiver_doc.reference.update(
                    {'balance.' + currency: receiver_balance + amount})
                receiver_transactions_ref.update({"status": True})

            return {'message': 'Transfer transaction created successfully'}, 200
        except Exception as e:
            return {"error": f"error happened at: {e}"}
