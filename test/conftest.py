from app import create_app, db
from app.models import Establishment
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class TestingConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/theorchard_test"
    
def reset_db():    
    db.session.rollback()
    db.session.execute("TRUNCATE TABLE establishment CASCADE")
    db.session.commit()

@pytest.fixture(scope="session")
def test_app():
    app = create_app(TestingConfig)
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    
    yield app
    
    ctx.pop()
    
@pytest.fixture
def test_db(test_app):
    reset_db()
    return db.session
