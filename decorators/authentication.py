import jwt
from functools import wraps
from flask import request, jsonify
from app import User, app


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
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query \
                .filter_by(public_id=data['public_id']) \
                .first()
        except Exception as err:
            return jsonify({
                'message': f'Token is invalid. Error {err.__str__()}'
            }), 401
        # returns the current logged user context to the routes
        return f(current_user, *args, **kwargs)

    return decorated
