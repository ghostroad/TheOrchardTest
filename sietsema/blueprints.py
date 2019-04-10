from flask import Blueprint, request, jsonify
from sietsema.models import Establishment, Rating, LatestRating
from sietsema.repositories import EstablishmentRepository
from sietsema import db
from sietsema.validations import validate, validate_date, validate_grade, validate_int
from dateutil.parser import parse
from sqlalchemy import or_

write_api = Blueprint('write_api', __name__)
establishment_repo = EstablishmentRepository(db.session)

@write_api.route('/establishments/<int:camis>', methods=['PUT'])
def establishment(camis):
    input = request.get_json()
    errors = validate(input, 
                valid_keys=['dba', 'boro', 'building', 'street', 'zipcode', 'phone', 'cuisine', 'inspection_date'],
                required_keys=['dba'], validations={'inspection_date': validate_date})
                
    if errors:
        return (jsonify(message=" ".join(errors)), 400)

    existing = establishment_repo.find(camis)
    if existing:
        return update_establishment(existing, input)
    else:
        establishment_repo.save(Establishment(camis=camis, **input))
        return jsonify(message="Created new establishment.")
        
        
@write_api.route('/establishments/<int:camis>/ratings', methods=['POST'])
def ratings(camis):
    input = request.get_json()
    errors = validate(input, 
                valid_keys=['grade', 'date'], required_keys=['grade', 'date'], validations={'date': validate_date, 'grade': validate_grade})
    
    if errors:
        return (jsonify(message=" ".join(errors)), 400)
    
    establishment = establishment_repo.find(camis)
    
    if not establishment: return (jsonify(message="No establishment with that camis exists."), 400)
    
    rating = establishment.ratings.filter_by(date=input['date']).all()
    if rating:
        return (jsonify(message="A rating already exists for that date."), 403)
    else:
        establishment.ratings.append(Rating(camis=camis, **input))
        db.session.commit()
        return jsonify(message="Created new rating.")
        

def update_establishment(establishment, input):
    new_inspection_date = ('inspection_date' in input) and parse(input['inspection_date']).date()
    if (new_inspection_date and ((establishment.inspection_date is None) or (establishment.inspection_date < new_inspection_date))):
        for attr in input:
            setattr(establishment, attr, input[attr])
            db.session.commit()
        return jsonify(message="Updated existing establishment.")
    else:
        return (jsonify(message="Must provide an inspection date that is newer than the current one."), 403)
    


read_api = Blueprint('read_api', __name__)
    
@read_api.route('/search', methods=['GET'])
def search():
    input = request.args
    errors = validate(input, 
                valid_keys=['after', 'limit', 'min_grade', 'cuisine'], 
                validations={'min_grade': validate_grade, 'after': validate_int, 'limit': validate_int})
                
    if errors:
        return (jsonify(message=" ".join(errors)), 400)
    
    conditions = assemble_conditions(input)
    
    limit = input.get('limit') or 20
    
    establishments = establishment_repo.latest_ratings_query().filter(*conditions).order_by(Establishment.camis).limit(limit).all()
    
    results = [search_result(establishment) for establishment in establishments]
    return jsonify(results)
    
def assemble_conditions(input):
    conditions = []
    min_grade = input.get('min_grade') or 'B'
    grade_options = [LatestRating.grade==grade for grade in ['A', 'B', 'C'] if grade <= min_grade]
    conditions.append(or_(*grade_options))
    
    if 'cuisine' in input:
        conditions.append(Establishment.cuisine==input['cuisine'])
    if 'after' in input:
        conditions.append(Establishment.camis > input['after'])
        
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
