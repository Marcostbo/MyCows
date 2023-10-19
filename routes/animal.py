from flask import Blueprint, jsonify, request, make_response
from datetime import datetime

from database import db
from decorators.authentication import token_required
from models import User, Animal
from models.animal import Kinship
from schemas.animal import AnimalSchema
from services.animal import AnimalService

animals_bp = Blueprint('animals', __name__)


@animals_bp.route('/get-animals', methods=['GET'])
@token_required
def get_all_animals(public_id):
    current_user = User.query.filter_by(public_id=public_id).first()
    animals = Animal.query.filter_by(owner=current_user)
    return jsonify(AnimalSchema(many=True).dump(obj=animals))


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
    data = request.form

    name = data.get('name')
    birth_date = datetime.strptime(data.get('birth_date'), '%Y-%m-%d').date()
    origin = data.get('origin')
    animal_type_id = data.get('animal_type_id')

    mother = father = None
    if data.get('mother_id'):
        mother = Animal.query.filter_by(id=data.get('mother_id')).first()
        if not mother:
            return make_response('Invalid ID for animal mother', 400)
    if data.get('father_id'):
        father = Animal.query.filter_by(id=data.get('father_id')).first()
        if not father:
            return make_response('Invalid ID for animal father', 400)

    animal_type = AnimalService.get_animal_type_by_id(
        type_id=int(animal_type_id)
    )

    new_animal = Animal(
        name=name,
        birth_date=birth_date,
        origin=origin,
        animal_type=animal_type,
        owner=current_user
    )
    # Register new animal for logged user
    db.session.add(new_animal)
    db.session.commit()

    if data.get('mother_id') or data.get('father_id'):
        new_kinship = Kinship(
            kid=new_animal,
            mother=mother,
            father=father
        )
        # Register new kinship for animal
        db.session.add(new_kinship)
        db.session.commit()
    return jsonify(AnimalSchema().dump(obj=new_animal))
