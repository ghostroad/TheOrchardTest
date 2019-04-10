from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

db = SQLAlchemy()

from sietsema.blueprints.read import read_api
from sietsema.blueprints.write import write_api


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if 'SIETSEMA_SETTINGS' in os.environ:
        app.config.from_envvar('SIETSEMA_SETTINGS')
    if test_config:
        app.config.from_object(test_config)

    app.register_blueprint(write_api)
    app.register_blueprint(read_api)

    db.init_app(app)
    return app


app = create_app()

migrate = Migrate(app, db)

from sietsema import models
