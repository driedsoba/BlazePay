# helpers.py
# This is for helper functions that don't fit in a specific module
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from flask_minimal.firebase import *

# require jwt to wrap
def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Verify JWT in the request
            verify_jwt_in_request()
            # If JWT is valid, call the protected route
            return fn(*args, **kwargs)
        except Exception as e:
            return {'error': 'JWT authentication required'}, 401
    return wrapper


def SearchUser(query):
    try:
        user_ref = db.collection("users")
        query = user_ref.where('phone', '==', query).limit(1).stream()
        doc_ids = []
        for doc in query:
            doc_ids.append(doc.id)
        if len(doc_ids) != 0:
            return doc_ids[0]
        else:
            return None
    except Exception as e:
        return {'error': str(e)}, 500
    
#return phone number:
def SearchNumber(query):
    try:
        user_ref = db.collection("users").document(query).get()
        return user_ref.get('phone')
    
    except Exception as e:
        return {'error': str(e)}, 500
