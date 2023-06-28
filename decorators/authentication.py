import jwt
import os
from functools import wraps
from flask import request, jsonify


# Decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except Exception as err:
            return jsonify({
                'message': f'Token is invalid. Error {err.__str__()}'
            }), 401
        # returns the current logged user context to the routes
        return f(data['public_id'], *args, **kwargs)

    return decorated
