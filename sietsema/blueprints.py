from flask import Blueprint, request, jsonify
from sietsema.models import Establishment
from sietsema import db

write_api = Blueprint('write_api', __name__)

@write_api.route('/health')
def health():
    return "Alive!"    

@write_api.route('/establishments/<int:camis>', methods=['PUT'])
def establishment(camis):
    input = request.get_json()
    errors = validate(input, 
                valid_keys=['dba', 'boro', 'building', 'street', 'zipcode', 'phone', 'cuisine'],
                required_keys=['dba'])
                
    if errors:
        return (jsonify(message=" ".join(errors)), 400)

    existing = Establishment.query.get(camis)
    if existing:
        for attr in input:
            setattr(existing, attr, input[attr])
        db.session.commit()
        return jsonify(message="Updated existing establishment.")
    else:
        db.session.add(Establishment(camis=camis, **input))
        db.session.commit()
        return jsonify(message="Created new establishment.")
    
def validate(input, valid_keys, required_keys=[]):
    errors = ["'{}' is an invalid key.".format(key) for key in input if key not in valid_keys]
    errors.extend(["The '{}' field cannot be empty.".format(key) for key in input if key in required_keys and not input[key]])
    return errors
    
    