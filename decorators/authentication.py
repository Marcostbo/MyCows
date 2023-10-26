from functools import wraps
from flask import request, jsonify
import jwt
import os


# Decorator to verify JWT in request
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')

        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            public_id = data.get('public_id')
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError as err:
            return jsonify({'message': f'Token is invalid. Error: {err}'}), 401

        return f(public_id, *args, **kwargs)
    return decorated
