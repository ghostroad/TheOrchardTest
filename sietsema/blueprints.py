from flask import Blueprint, request, jsonify
from sietsema.models import Establishment
from sietsema import db
from sietsema.validations import validate, validate_date
from dateutil.parser import parse

write_api = Blueprint('write_api', __name__)

@write_api.route('/health')
def health():
    return "Alive!"    

@write_api.route('/establishments/<int:camis>', methods=['PUT'])
def establishment(camis):
    input = request.get_json()
    errors = validate(input, 
                valid_keys=['dba', 'boro', 'building', 'street', 'zipcode', 'phone', 'cuisine', 'inspection_date'],
                required_keys=['dba'], validations={'inspection_date': validate_date})
                
    if errors:
        return (jsonify(message=" ".join(errors)), 400)

    existing = Establishment.query.get(camis)
    if existing:
        return update_establishment(existing, input)
    else:
        db.session.add(Establishment(camis=camis, **input))
        db.session.commit()
        return jsonify(message="Created new establishment.")
        
def update_establishment(establishment, input):
    new_inspection_date = ('inspection_date' in input) and parse(input['inspection_date']).date()
    if (new_inspection_date and ((establishment.inspection_date is None) or (establishment.inspection_date < new_inspection_date))):
        for attr in input:
            setattr(establishment, attr, input[attr])
            db.session.commit()
        return jsonify(message="Updated existing establishment.")
    else:
        return (jsonify(message="Must provide an inspection date that is newer than the current one."), 403)
    
    
