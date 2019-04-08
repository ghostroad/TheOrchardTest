from flask import Flask
from config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig)
    if test_config:
        app.config.from_object(test_config)
    db.init_app(app)
    return app
    
app = create_app()
    
migrate = Migrate(app, db)

from app import routes, models