from flask import Blueprint, jsonify, request, make_response, abort
from marshmallow import ValidationError

from decorators.authentication import token_required
from enums.animal import AnimalType
from models import User, Animal
from schemas.animal import BaseAnimalSchema, AnimalSchema, CreateAnimalSchema, UpdateAnimalSchema, BaseDashboardSchema, \
    AnimalQuerySchema
from services.animal import AnimalService
from sqlalchemy import func

animals_bp = Blueprint('animals', __name__)


@animals_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard(public_id: str):
    animals = Animal.query.join(User).filter(User.public_id == public_id)

    # Group animals by sex
    animals_by_sex = animals.with_entities(
        Animal.animal_sex,
        func.count(Animal.animal_sex)
    ).group_by(
        Animal.animal_sex
    ).all()

    # Group animals by type
    animals_by_type = animals.with_entities(
        Animal.animal_type,
        func.count(Animal.animal_type)
    ).group_by(
        Animal.animal_type
    ).all()

    sex_data = BaseDashboardSchema(many=True).dump([
        {'type': item[0].name, 'count': item[1]} for item in animals_by_sex
    ])

    type_data = BaseDashboardSchema(many=True).dump([
        {'type': item[0].name, 'count': item[1]} for item in animals_by_type
    ])

    return jsonify({'animals_by_sex': sex_data, 'animals_by_type': type_data})


@animals_bp.route('/animals', methods=['GET'])
@token_required
def get_all_animals(public_id: str):
    # current_user = User.query.filter_by(public_id=public_id).first()
    # animals = Animal.query.filter_by(owner=current_user)
    try:
        query_params = AnimalQuerySchema().load(data=request.args)
        name = query_params.get('name')
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    animals = Animal.query.join(User).filter(User.public_id == public_id)
    if name:
        animals = animals.filter(Animal.name == name)
    return jsonify(BaseAnimalSchema(many=True).dump(obj=animals))


@animals_bp.route('/animals/<animal_id>', methods=['GET'])
@token_required
def get_animal_by_id(public_id: str, animal_id: int):
    animal: Animal = Animal.query.join(
        User, Animal.owner_id == User.id
    ).filter(
        User.public_id == public_id, Animal.id == animal_id
    ).first_or_404(description='Animal not found')
    return jsonify(AnimalSchema().dump(obj=animal))


@animals_bp.route('/animals/<animal_id>', methods=['PUT'])
@token_required
def update_animal(public_id: str, animal_id: int):
    validated_data = UpdateAnimalSchema().load(request.form)

    animal: Animal = Animal.query.join(User).filter(User.public_id == public_id, Animal.id == animal_id).first()
    if not animal:
        abort(403, 'Permission Denied')

    animal.update(
        **validated_data
    )
    return jsonify(AnimalSchema().dump(obj=animal))


@animals_bp.route('/animals', methods=['POST'])
@token_required
def register_animal(public_id: str):
    current_user: User = User.query.filter_by(public_id=public_id).first()
    validated_data = CreateAnimalSchema().load(request.form)

    mother: Animal | None = None
    father: Animal | None = None
    if validated_data.get('mother_id'):
        mother: Animal = Animal.query.filter_by(id=validated_data.get('mother_id')).first()
        if not mother:
            return make_response('Invalid ID for animal mother', 400)
    if validated_data.get('father_id'):
        father: Animal = Animal.query.filter_by(id=validated_data.get('father_id')).first()
        if not father:
            return make_response('Invalid ID for animal father', 400)

    animal_type: AnimalType = AnimalService.get_animal_type_by_id(
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
    new_animal.save()
    return jsonify(AnimalSchema().dump(obj=new_animal))
