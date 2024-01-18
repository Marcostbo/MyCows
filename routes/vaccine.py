from flask import Blueprint, jsonify, request, make_response, abort

from decorators.authentication import token_required
from models import Animal, User, Vaccine
from models.animal import AnimalVaccination
from schemas.vaccine import AnimalVaccinationCreationSchema, AnimalVaccinationSchema, VaccineSchema
from services.animal import AnimalService

vaccine_bp = Blueprint('vaccine', __name__)


@vaccine_bp.route('/vaccines', methods=['GET'])
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

    if not any(Animal.query.join(User).filter(User.public_id == public_id, Animal.id == animal_id)):
        abort(403, 'Permission Denied')

    if not any(Vaccine.query.filter_by(id=vaccine_id)):
        abort(400, 'Invalid Vaccine')

    animal_vaccination = AnimalVaccination(
        animal_id=animal_id,
        vaccine_id=vaccine_id,
        vaccinated_on=validated_data.get('vaccinated_on')
    )
    animal_vaccination.save()

    return make_response('', 201)


@vaccine_bp.route('/vaccinations', methods=['GET'])
@token_required
def get_vaccinations(public_id: str):
    vaccinations = AnimalVaccination.query\
        .join(Animal, AnimalVaccination.animal_id == Animal.id)\
        .join(Vaccine, AnimalVaccination.vaccine_id == Vaccine.id)\
        .join(User, Animal.owner_id == User.id)\
        .filter(User.public_id == public_id)
    return jsonify(AnimalVaccinationSchema().dump(obj=vaccinations, many=True))
