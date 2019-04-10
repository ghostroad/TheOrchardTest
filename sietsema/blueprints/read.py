from flask import Blueprint, request, jsonify
from sietsema.models import Establishment, LatestRating
from sietsema.repositories import EstablishmentRepository
from sietsema import db
from sietsema.validations import validate, validate_grade, validate_int
from sqlalchemy import or_

read_api = Blueprint('read_api', __name__)
establishment_repo = EstablishmentRepository(db.session)


@read_api.route('/search', methods=['GET'])
def search():
    input_data = request.args
    errors = validate(input_data,
                      valid_keys=['after', 'limit', 'min_grade', 'cuisine'],
                      validations={'min_grade': validate_grade, 'after': validate_int, 'limit': validate_int})

    if errors:
        return jsonify(message=" ".join(errors)), 400

    conditions = assemble_conditions(input_data)

    limit = input_data.get('limit') or 20

    establishments = establishment_repo.latest_ratings_query().filter(*conditions).order_by(Establishment.camis).limit(
        limit).all()

    results = [search_result(establishment) for establishment in establishments]
    return jsonify(results)


def assemble_conditions(input_data):
    conditions = []
    min_grade = input_data.get('min_grade') or 'B'
    grade_options = [LatestRating.grade == grade for grade in ['A', 'B', 'C'] if grade <= min_grade]
    conditions.append(or_(*grade_options))

    if 'cuisine' in input_data:
        conditions.append(Establishment.cuisine == input_data['cuisine'])
    if 'after' in input_data:
        conditions.append(Establishment.camis > input_data['after'])

    return conditions


def search_result(establishment):
    return dict(
        camis=establishment.camis,
        dba=establishment.dba,
        boro=establishment.boro,
        building=establishment.building,
        street=establishment.street,
        zipcode=establishment.zipcode,
        phone=establishment.phone,
        cuisine=establishment.cuisine,
        latest_grade=establishment.latest_rating.grade,
        latest_grade_date=establishment.latest_rating.date
    )
