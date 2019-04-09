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
    errors = validate_parameters(data, 
                valid_keys=['dba', 'boro', 'building', 'street', 'zipcode', 'phone', 'cuisine'],
                required_keys=['dba'])
                
    if errors:
        return (jsonify(message=" ".join(errors)), 400)

    existing = Establishment.query.get(camis)
    if existing:
        for attr in data:
            setattr(existing, attr, data[attr])
        db.session.commit()
        return jsonify(message="Updated existing establishment.")
    else:
        db.session.add(Establishment(camis=camis, **data))
        db.session.commit()
        return jsonify(message="Created new establishment.")
    
def validate_parameters(parameters, valid_keys, required_keys=[]):
    errors = ["'{}' is an invalid key.".format(key) for key in parameters if key not in valid_keys]
    errors.extend(["The '{}' field cannot be empty.".format(key) for key in parameters if key in required_keys and not parameters[key]])
    return errors
    
    