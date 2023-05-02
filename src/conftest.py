import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from src.apps.faces.api.routing import api_face
from src.apps.faces import models as faces_models  # noqa: F401


@pytest.fixture(scope="session")
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.register_blueprint(api_face)
    return app


@pytest.fixture(scope="session")
def engine(app):
    engine = create_engine("sqlite:///test.db")
    return engine


@pytest.fixture(scope="session")
def db(app):
    db = SQLAlchemy(app=app)
    return db


@pytest.fixture(scope="function")
def session(db, engine):
    db.metadata.create_all(bind=engine)
    session = db.session
    session.begin_nested()
    yield session
    session.rollback()


@pytest.fixture()
def client(app):
    return app.test_client()
