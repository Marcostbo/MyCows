from flask import Blueprint, jsonify

from decorators.authentication import token_required
from schemas.ima_report import ImaReportSchema
from services.ima_report_service import IMAReportService

ima_bp = Blueprint('ima', __name__)


@ima_bp.route('/ima-report', methods=['GET'])
@token_required
def ima_report(public_id):
    report = IMAReportService.build_ima_report(public_id=public_id)
    return jsonify(ImaReportSchema().dump(obj=report))
