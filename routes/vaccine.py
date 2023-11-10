from flask import Blueprint, jsonify, request, make_response, abort

from decorators.authentication import token_required
from models import Animal, User, Vaccine
from models.animal import AnimalVaccination
from schemas.vaccine import AnimalVaccinationCreationSchema, AnimalVaccinationSchema, VaccineSchema
from services.animal import AnimalService

vaccine_bp = Blueprint('vaccine', __name__)


@vaccine_bp.route('/vaccines-list', methods=['GET'])
def list_vaccines():
    return make_response(
        jsonify(VaccineSchema().dump(obj=Vaccine.query.all(), many=True))
    )


@vaccine_bp.route('/vaccinate-animal', methods=['POST'])
@token_required
def vaccinate_animal(public_id: str):
    validated_data = AnimalVaccinationCreationSchema().load(request.form)
    animal_id: int = validated_data.get('animal_id')
    vaccine_id: int = validated_data.get('vaccine_id')

    animal: Animal = Animal.query.join(User).filter(User.public_id == public_id, Animal.id == animal_id).first()
    if not animal:
        abort(403, 'Permission Denied')

    vaccine: Vaccine = Vaccine.query.filter_by(id=vaccine_id).first()
    if not vaccine:
        abort(400, 'Invalid Vaccine')

    animal_vaccination = AnimalVaccination(
        animal_id=animal_id,
        vaccine_id=vaccine_id,
        vaccinated_on=validated_data.get('vaccinated_on')
    )
    animal_vaccination.save()

    return make_response(jsonify(AnimalVaccinationSchema().dump({
        'animal': animal,
        'vaccine': vaccine,
        'vaccinated_on': validated_data.get('vaccinated_on')}
    )
    ), 201)
