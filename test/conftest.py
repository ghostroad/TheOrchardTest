import pytest

from sietsema import create_app, db
from sietsema.repositories import EstablishmentRepository


class TestingConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/sietsema_test"
    SQLALCHEMY_ECHO = False # set to True to log all SQL statements
    
def reset_db():
    db.session.rollback() # needed in case the session is in a bad state
    db.session.execute("TRUNCATE TABLE establishment CASCADE")
    db.session.commit()

@pytest.fixture(scope="session")
def test_app():
    app = create_app(TestingConfig)
    context = app.app_context()
    context.push()
    db.drop_all()
    db.create_all()
    
    yield app
    
    context.pop()
    
@pytest.fixture(scope="session")
def test_client(test_app):
    return test_app.test_client()
        
    
@pytest.fixture
def test_db(test_app): 
    # Even though the method parameter is unused, requiring it initializes the test app,
    # which must be done prior to any db operation.
    reset_db()
    return db.session

@pytest.fixture
def repo(test_db):
    return EstablishmentRepository(test_db)
