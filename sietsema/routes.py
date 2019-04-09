from sietsema import app
from sietsema.models import Establishment

@app.route('/')
@app.route('/index')
def index():
    return "\n".join([str(est) for est in Establishment.query.all()])
    
    
@app.route('/establishment', methods=['POST'])
def establishment():
    data = flask.request.get_json()
    print(data)
    return "Thanks!"