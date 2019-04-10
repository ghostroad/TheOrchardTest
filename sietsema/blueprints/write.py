from flask import Blueprint, request, jsonify
from sietsema.models import Establishment, Rating
from sietsema.repositories import EstablishmentRepository
from sietsema import db
from sietsema.validations import validate, validate_date, validate_grade
from dateutil.parser import parse
from functools import wraps


def expects_json(inner):
    @wraps(inner)
    def wrapped(*args, **kwargs):
        if not request.get_json():
            return jsonify(message="Expects a JSON body."), 400
        return inner(*args, **kwargs)

    return wrapped


write_api = Blueprint('write_api', __name__)
establishment_repo = EstablishmentRepository(db.session)


@write_api.route('/establishments/<int:camis>', methods=['PUT'])
@expects_json
def establishment(camis):
    input_data = request.get_json()
    errors = validate(input_data,
                      valid_keys=['dba', 'boro', 'building', 'street', 'zipcode', 'phone', 'cuisine',
                                  'inspection_date'],
                      required_keys=['dba'],
                      validations={'inspection_date': validate_date})

    if errors:
        return jsonify(message=" ".join(errors)), 400

    existing = establishment_repo.find(camis)
    if existing:
        return update_establishment(existing, input_data)
    else:
        establishment_repo.save(Establishment(camis=camis, **input_data))
        return jsonify(message="Created new establishment.")


@write_api.route('/establishments/<int:camis>/ratings', methods=['POST'])
@expects_json
def ratings(camis):
    input_data = request.get_json()
    errors = validate(input_data,
                      valid_keys=['grade', 'date'],
                      required_keys=['grade', 'date'],
                      validations={'date': validate_date, 'grade': validate_grade})

    if errors:
        return jsonify(message=" ".join(errors)), 400

    existing = establishment_repo.find(camis)

    if not existing:
        return jsonify(message="No establishment with that camis exists."), 400

    rating = existing.ratings.filter_by(date=input_data['date']).all()
    if rating:
        return jsonify(message="A rating already exists for that date."), 403
    else:
        existing.ratings.append(Rating(camis=camis, **input_data))
        db.session.commit()
        return jsonify(message="Created new rating.")


def update_establishment(existing, input_data):
    new_inspection_date = ('inspection_date' in input_data) and parse(input_data['inspection_date']).date()
    if (new_inspection_date and (
            (existing.inspection_date is None) or (existing.inspection_date < new_inspection_date))):
        for attr in input_data:
            setattr(existing, attr, input_data[attr])
            db.session.commit()
        return jsonify(message="Updated existing establishment.")
    else:
        return jsonify(message="Must provide an inspection date that is newer than the current one."), 403
