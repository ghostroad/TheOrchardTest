from flask import Blueprint, request
from sietsema.models import Establishment
from sietsema import db

write_api = Blueprint('write_api', __name__)

@write_api.route('/health')
def health():
    return "Alive!"    

@app.route('/establishment/<int:camis>', methods=['PUT'])
def establishment(camis):
    data = flask.request.get_json()
    db.session.add(Establishment(data))
    db.session.commit()
    return 200