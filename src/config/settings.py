import os

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

DEBUG = os.environ.get("DEBUG", True)

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./sql_app.db")
DLIB_MODEL_PATH = os.environ.get(
    "DLIB_SHAPE_PREDICTOR", "shape_predictor_5_face_landmarks.dat"
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db = SQLAlchemy(app)
ma = Marshmallow(app)
