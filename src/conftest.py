import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture(scope="session")
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    return app


@pytest.fixture(scope="session")
def db(app):
    db = SQLAlchemy(app=app)
    return db


@pytest.fixture(scope="function")
def session(db):
    session = db.session
    session.begin_nested()
    yield session
    session.rollback()


@pytest.fixture()
def client(app):
    return app.test_client()
