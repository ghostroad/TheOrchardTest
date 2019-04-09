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

    dba = data['dba']
    if not dba:
        return (jsonify(message="The 'dba' field cannot be empty."), 400)

    existing = Establishment.query.get(camis)
    if existing:
        for attr in ['dba', 'boro', 'building', 'street', 'zipcode', 'phone', 'cuisine']:
            if attr in data:
                setattr(existing, attr, data[attr])
        db.session.commit()
        return jsonify(message="Updated existing establishment.")
    else:
        db.session.add(Establishment(camis=camis, **data))
        db.session.commit()
        return jsonify(message="Created new establishment.")
    
    