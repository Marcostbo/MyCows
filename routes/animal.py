from flask import Blueprint, jsonify, request, make_response
from datetime import datetime

from database import db
from decorators.authentication import token_required
from models import User, Animal
from schemas.animal import BaseAnimalSchema, AnimalSchema, CreateAnimalSchema
from services.animal import AnimalService

animals_bp = Blueprint('animals', __name__)


@animals_bp.route('/get-animals', methods=['GET'])
@token_required
def get_all_animals(public_id):
    # current_user = User.query.filter_by(public_id=public_id).first()
    # animals = Animal.query.filter_by(owner=current_user)
    animals = Animal.query.join(User).filter_by(public_id=public_id)
    return jsonify(BaseAnimalSchema(many=True).dump(obj=animals))


@animals_bp.route('/get-animals/<animal_id>', methods=['GET'])
@token_required
def get_animal_by_id(public_id, animal_id):
    current_user = User.query.filter_by(public_id=public_id).first()
    animal = Animal.query.filter_by(owner=current_user).filter_by(id=animal_id).first()
    return jsonify(AnimalSchema().dump(obj=animal))


@animals_bp.route('/register-animal', methods=['POST'])
@token_required
def register_animal(public_id):
    current_user = User.query.filter_by(public_id=public_id).first()
    validated_data = CreateAnimalSchema().load(request.form)

    mother = father = None
    if validated_data.get('mother_id'):
        mother = Animal.query.filter_by(id=validated_data.get('mother_id')).first()
        if not mother:
            return make_response('Invalid ID for animal mother', 400)
    if validated_data.get('father_id'):
        father = Animal.query.filter_by(id=validated_data.get('father_id')).first()
        if not father:
            return make_response('Invalid ID for animal father', 400)

    animal_type = AnimalService.get_animal_type_by_id(
        type_id=validated_data.get('animal_type_id')
    )

    new_animal = Animal(
        name=validated_data.get('name'),
        birth_date=validated_data.get('birth_date'),
        origin=validated_data.get('origin'),
        animal_type=animal_type,
        owner=current_user,
        mother=mother,
        father=father
    )
    # Register new animal for logged user
    db.session.add(new_animal)
    db.session.commit()
    return jsonify(AnimalSchema().dump(obj=new_animal))
