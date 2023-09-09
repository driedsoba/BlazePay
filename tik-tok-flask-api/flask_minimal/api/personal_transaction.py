from flask_restful import Resource, Api, fields, abort, reqparse
from flask import request
import json
import bcrypt
import uuid
import stripe

# FIREBASE DEP
import firebase_admin
from firebase_admin import credentials, firestore, db
from flask_minimal.firebase import db
from flask_minimal.helpers import jwt_required_custom
from flask_jwt_extended import create_access_token, get_jwt_identity

# cred initialization - to comment out
stripe.api_key = '[INSERT STRIPE TOKEN]'


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
                'groups': []
            })
            return {'message': 'User registered successfully'}, 200
        except Exception as e:
            return {"error": f"error happened at creating user, {e}"}

# GET API to search for user document id


class SearchUser(Resource):
    def post(self):
        try:
            user_data = request.get_json(force=True)
            search_query = user_data['user']

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
    def post(self):
        try:
            profile_parameters = request.get_json(force=True)
            phone = profile_parameters['phone']
            pin = profile_parameters['pin']

            if not (phone and pin):
                return {'error': 'Phone and Pin query are required'}, 400

            user_ref = db.collection("users")
            query = user_ref.where('phone', '==', phone)
            query = query.stream()
            query_results = list(query)

            if not query_results:
                return {'error': 'Phone number does not exist'}, 400

            # Iterate through the query results
            for doc in query_results:
                user_data = doc.to_dict()
                user_id = doc.id
                hashed_pin = user_data.get('hashed_pin', '')

            if bcrypt.checkpw(pin.encode('utf-8'), hashed_pin.encode('utf-8')):
                # PIN matches, return user data without PIN and salt
                user_data.pop('hashed_pin', None)
                user_data.pop('salt', None)
                user_data.pop('transaction', None)

                # JWT Token
                access_token = create_access_token(identity=user_id)
                return {'message': 'PIN matches, data returned', 'user_data': user_data, 'access_token': access_token}, 200
            else:
                return {'error': 'Credentials not matched/found'}, 404
        except Exception as e:
            return {'error': str(e)}, 500


class GetData(Resource):
    @jwt_required_custom
    def post(self):
        try:
            current_user = get_jwt_identity()
            user_data = db.collection("users").document(
                current_user).get().to_dict()
            print(user_data)
            user_data.pop('hashed_pin', None)
            user_data.pop('salt', None)
            user_data.pop('transaction', None)
            print(user_data)

            return {'message': 'PIN matches, data returned', 'user_data': user_data}, 200

        except Exception as e:
            return {'error': str(e)}, 500


class CreateStripePayment(Resource):
    def post(self):
        try:
            topup_parameters = request.get_json(force=True)

            amount = topup_parameters['amount']
            currency = topup_parameters['currency'].upper()

        except Exception as e:
            return {'error': str(e)}, 500


class stripe_webhook(Resource):
    def post(self):
        payload = request.get_data(as_text=True)
        sig_header = request.headers.get("Stripe-Signature")
        json_payload = json.loads(payload)

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, 'whsec_6e512dcf7620722751acbd679467d53df8d76cdf314ff95466712068f3fd466a'
            )

        except ValueError as e:
            # Invalid payload
            return "Invalid payload", 400
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return "Invalid signature", 400

        # Handle the checkout.session.completed event
        if event["type"] == "checkout.session.completed":
            print("Payment was successful.")

            user_ref = db.collection("users")
            currency = json_payload['data']['object']['currency'].upper()

            query = db.collection('transactions').where(
                "stripe_session_id", "==", json_payload['data']['object']['id']).limit(1).stream()

            if query:

                for doc in query:
                    print("Stripe transaction ID found!")
                    doc_id = doc.id
                    doc_object = doc.to_dict()
                    print(doc_object)
                    account = doc_object['transaction_acc']
                    transaction_amount = doc_object['amount']

                    # GET THE REFERENCE TO BE UPDATED
                    doc_ref = db.collection(
                        'transactions').document(doc_id).get()
                    doc_ref.reference.update({"status": True})

                    acc_doc = user_ref.document(account).get()
                    prefix_to_search = [account]
                    total_balance = {}
                    for prefix in prefix_to_search:
                        query = db.collection('transactions').where(
                            "transaction_acc", "==", prefix).where("status", "==", True)
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

                    acc_balance = acc_doc.get('balance').get(currency)
                    print(acc_balance)
                    print(transaction_amount)
                    print(total_balance[account])

                    if total_balance[account] == acc_balance+transaction_amount:
                        acc_doc.reference.update(
                            {'balance.' + currency: acc_balance + transaction_amount})
                    else:
                        return {'error': 'Balance does not tally'}, 404
                    break

            else:
                return {'error': 'Transaction not matched/found'}, 404

        return "Success", 200


class TopUp(Resource):
    @jwt_required_custom
    def post(self):
        try:
            current_user = get_jwt_identity()
            account = current_user
            topup_parameters = request.get_json(force=True)
            amount = topup_parameters['amount']
            currency = topup_parameters['currency'].upper()
            transaction_id = str(uuid.uuid4())

            user_ref = db.collection("users")
            acc_doc = user_ref.document(account).get()

            if not acc_doc.exists:
                return {'error': 'Account does not exist, check whether acc is still valid'}, 404

            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'product_data': {
                            'name': 'TopUp',
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 100,
                }],
                mode='payment',
                success_url='http://localhost:3000/home',
                cancel_url='http://localhost:3000/',
            )

            # return {'stripe_url': session.url, "sessionId": session["id"]}, 201

            # Iterate through the query results
            account_transactions_ref = db.collection(
                'transactions').document(account+'-'+transaction_id)
            account_transactions_ref.set({
                'transaction_acc': account,
                'amount': amount,  # Debit amount is negative
                'currency': currency,
                'type': 'debit',
                'mode': 'topup',
                'stripe_session_id': session['id'],
                'status': False
            })

            # Update user balances using double-entry accounting

            return {'stripe_url': session.url, "sessionId": session["id"]}, 200

        except Exception as e:
            return {'error': str(e)}, 500
