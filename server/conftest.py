import pytest
from app import app as flask_app
from models import db as _db

@pytest.fixture
def app():
    # Setup the temporary testing environment
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture
def client(app):
    # This simulates a browser/frontend sending requests (for test_app.py)
    return app.test_client()

@pytest.fixture
def db(app):
    # This gives us direct access to the database (for test_models.py)
    return _db