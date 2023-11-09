from flask import Blueprint, jsonify

from decorators.authentication import token_required
from models import User, Animal
from schemas.ima_report import ImaReportSchema

ima_bp = Blueprint('ima', __name__)


@ima_bp.route('/ima-report', methods=['GET'])
@token_required
def ima_report(public_id):
    animals = Animal.query.join(User).filter(User.public_id == public_id)
    report: dict[str, int] = {
        'male_00_12': animals.filter(Animal.animal_sex == 'Male').count(),
        'female_00_12': animals.filter(Animal.animal_sex == 'Female').count()
    }
    return jsonify(ImaReportSchema().dump(obj=report))
