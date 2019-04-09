from flask import Blueprint, request, jsonify
from sietsema.models import Establishment
from sietsema import db

write_api = Blueprint('write_api', __name__)

@write_api.route('/health')
def health():
    return "Alive!"    

@write_api.route('/establishment/<int:camis>', methods=['PUT'])
def establishment(camis):
    data = request.get_json()
    db.session.add(Establishment(camis=camis, **data))
    db.session.commit()
    return jsonify(success=True)