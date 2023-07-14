import os
import uuid
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash

from database import db
from decorators.authentication import token_required
from models import User, Cow

cows_bp = Blueprint('cows', __name__)


@cows_bp.route('/get-cows', methods=['GET'])
@token_required
def get_all_cows(public_id):
    current_user = User.query.filter_by(public_id=public_id).first()
    cows = Cow.query.filter_by(owner=current_user)
    response = [cow.simple_serialize for cow in cows]
    return jsonify({'cows': response})


@cows_bp.route('/register-cow', methods=['POST'])
@token_required
def register_cow(public_id):
    current_user = User.query.filter_by(public_id=public_id).first()
    data = request.form
    cow_name = data.get('name')

    new_cow = Cow(
        name=cow_name,
        owner=current_user
    )
    # Register new cow for logged user
    db.session.add(new_cow)
    db.session.commit()
    return jsonify({'cow': new_cow.simple_serialize})
