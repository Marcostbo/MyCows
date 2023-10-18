from flask import Blueprint, jsonify, request

from database import db
from decorators.authentication import token_required
from models import User, Animal

cows_bp = Blueprint('cows', __name__)


@cows_bp.route('/get-animals', methods=['GET'])
@token_required
def get_all_animals(public_id):
    current_user = User.query.filter_by(public_id=public_id).first()
    cows = Animal.query.filter_by(owner=current_user)
    response = [cow.simple_serialize for cow in cows]
    return jsonify({'cows': response})


@cows_bp.route('/get-animals/<animal_id>', methods=['GET'])
@token_required
def get_cow_by_id(public_id, animal_id):
    current_user = User.query.filter_by(public_id=public_id).first()
    animal = Animal.query.filter_by(owner=current_user).filter_by(id=animal_id).first()
    return jsonify({'cows': animal.simple_serialize})


@cows_bp.route('/register-cow', methods=['POST'])
@token_required
def register_cow(public_id):
    current_user = User.query.filter_by(public_id=public_id).first()
    data = request.form
    animal_name = data.get('name')

    new_animal = Animal(
        name=animal_name,
        owner=current_user
    )
    # Register new cow for logged user
    db.session.add(new_animal)
    db.session.commit()
    return jsonify({'cow': new_animal.simple_serialize})
