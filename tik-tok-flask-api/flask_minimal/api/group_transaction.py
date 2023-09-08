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
from flask_minimal.helpers import jwt_required_custom, SearchUser, SearchNumber
from flask_jwt_extended import create_access_token, get_jwt_identity

# cred initialization - to comment out

### Group payment APIs: Create, Modify, Retrieve Info
class CreateGroupTransaction(Resource):
    @jwt_required_custom
    def post(self):
        try:
            transaction_parameters = request.get_json(force=True)
            current_user = get_jwt_identity()
            requestor = current_user
            name = transaction_parameters['name']
            members = transaction_parameters['members']
            amount = transaction_parameters['amount']
            currency = transaction_parameters['currency'].upper()
            group_transaction_id = str(uuid.uuid4())

            users_ref = db.collection('users')
            requestor_doc = users_ref.document(requestor).get()

            if not requestor_doc.exists:
                return {'error': 'Requestor or receiver does not exist, invalid'}, 404
            
            #verify all members exist
            member_ids=[]
            for member in members:
                member_id= SearchUser(member)
                member_ids.append(member_id)
                member_doc = users_ref.document(member_id).get()
                if not member_doc.exists:
                    return {'error': 'Group member receiver does not exist, invalid'}, 404
                else:
                    print('alls good')

            # Check if group name by this certain requestor has already existed
            name_query =  db.collection('groups').where('name', '==', name).where('requestor', '==', requestor).get()
            if name_query:
                return {'error': 'Group Name already exists'}, 400
            
            ## include in group list
            for member in member_ids:
                member_doc = users_ref.document(member).get()
                member_data= member_doc.to_dict()
                data=(member_data.get('groups'))
                data.append(group_transaction_id)
                member_doc.reference.update({"groups": data})

            num_members = len(member_ids)
            share_per_member = amount / num_members

            # Create a dictionary to store individual transactions
            transaction_list = {}

            # Add transactions for each member
            for member in members:
                transaction_list[member] = share_per_member

            group_transactions_ref = db.collection('groups').document(group_transaction_id)
            group_transactions_ref.set({
                'name': name,
                'requestor': requestor,
                'group_id': group_transaction_id,
                'members': members,
                'amount': amount,  # Debit amount is negative
                'currency': currency,
                'transactions': transaction_list,
                'status':False
            })
            return  {'message': 'Group Payment has been created successfully'}, 201
        except Exception as e:
            return {"error": f"error happened at: {e}"}
        
class CheckGroupTransaction(Resource):
    @jwt_required_custom
    def post(self):
            try:
                transaction_parameters = request.get_json(force=True)
                current_user = get_jwt_identity()
                requestor = current_user
                group_id = transaction_parameters['group_id']
                distribution = transaction_parameters['distribution']

                ## must check if the user is the requestor, only requestor can modify
                if requestor!= db.collection('groups').document(group_id).get().get('requestor'):
                    return {'error': 'Only Requestor can modify the distribution'}, 400

                if(sum(distribution.values()))==db.collection('groups').document(group_id).get().get('amount'):
                    group_transactions_ref = db.collection('groups').document(group_id).get()
                    group_transactions_ref.reference.update({"transactions": distribution})
                    return {'message': 'Group Payment has been updated successfully'}, 201
                
                else:
                    return {'message': 'Sth wrong with distribution'}, 400

            except Exception as e:
                return {'error': str(e)}, 500
            
    def get(self):
        try:
            name = request.args.get('name')
            client = request.args.get('client')

            group_query = db.collection('groups').where('name', '==', name).get()

            # Check if the document exists
            if not group_query:
                return {'error': 'Group not found'}, 404

            group_info=None
            # Check if requestor matches the requestor field
            for group_doc in group_query:
                # Check if the requestor is in the list of members
                group_info=group_doc.to_dict()
                members = group_doc.get('members')
                if group_doc.get("requestor")==client:
                    continue
                elif client in members:
                    continue
                else:
                    return {'error': 'Invalid group requestor'}, 404
            # Requestor is a member of the group, return a success response
            if group_info:
                # Return group info along with a success response
                return {'message': 'Requestor is valid for this group', 'group_id': group_info['group_id'],'transactions':group_info['transactions']}, 200
            else:
                # If requestor is not found in any matching group document, return a 403 response
                return {'error': 'Requestor is not a member of the group'}, 403
            
        except Exception as e:
            return {'error': str(e)}, 500
        
class ProcessGroupPayment(Resource):
    @jwt_required_custom
    def post(self):
        try:
            transaction_parameters = request.get_json(force=True)
            current_user = get_jwt_identity()
            member = current_user
            group_id = transaction_parameters['group_id']
            transaction_id = str(uuid.uuid4())
            
            #check for how much user need to pay:
            groups_ref = db.collection('groups')
            group_doc = groups_ref.document(group_id).get()

            # group related info:
            currency = group_doc.get('currency')
            requestor = group_doc.get('requestor')

            print(group_doc.get('members'))

            #check for user info
            users_ref = db.collection('users')
            member_doc = users_ref.document(member).get()
            group_transaction = group_doc.get('transactions')

            member = SearchNumber(member)
            if member in group_doc.get('members'):
                amount_payable =  group_doc.get('transactions')[member]
            else: 
                return {'error': 'You are not in the group'}, 404
            #requestor
            requestor_doc = users_ref.document(group_doc.get('requestor')).get()

            ## must check if the user is the requestor, only requestor can modify
            if member_doc.get('balance').get(currency)<group_doc.get('transactions')[member]:
                return {'error': 'You dont have enough money, please top up'}, 404
            else:
                pass

            member_transactions_ref = db.collection('transactions').document(member+'-'+transaction_id)
            member_transactions_ref.set({
                'transaction_acc': member,
                'receiver_user_id': requestor,
                'sender_user_id': member,
                'amount': amount_payable,  # Debit amount is negative
                'currency': currency,
                'type': 'credit',
                'mode':'Group',
                'status':False
            })

            requestor_transactions_ref = db.collection('transactions').document(requestor+'-'+transaction_id)
            requestor_transactions_ref.set({
                'transaction_acc': member,
                'receiver_user_id': requestor,
                'sender_user_id': member,
                'amount': amount_payable,  # Debit amount is negative
                'currency': currency,
                'type': 'credit',
                'mode':'Group',
                'status':False
            })


            # Update user balances using double-entry accounting
            member_balance = member_doc.get('balance').get(currency)
            requestor_balance = requestor_doc.get('balance').get(currency)

            # if total_balance[member]==member_balance-amount:
            member_doc.reference.update({'balance.' + currency: member_balance - amount_payable})
            member_transactions_ref.update({ "status": True})

            # if total_balance[requestor]==requestor_balance+amount:
            requestor_doc.reference.update({'balance.' + currency: requestor_balance + amount_payable})
            requestor_transactions_ref.update({ "status": True})

            group_transaction.pop(member)
            group_doc.reference.update({"transactions": group_transaction})
            if len(group_transaction) == 0:
                group_doc.reference.update({"status": True})
            # update transaction in transaction collection:
            
            return {'message': 'I paid my part, thank you'}, 201

        except Exception as e:
            return {'error': str(e)}, 500
            
