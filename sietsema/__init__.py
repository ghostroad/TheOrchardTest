import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from flask import Flask
from config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

from sietsema.blueprints import write_api, read_api

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig)
    app.register_blueprint(write_api)
    app.register_blueprint(read_api)
    
    if test_config:
        app.config.from_object(test_config)
    db.init_app(app)
    return app
    
app = create_app()
    
migrate = Migrate(app, db)

from sietsema import models