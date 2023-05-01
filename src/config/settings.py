import os

DEBUG = os.environ.get("DEBUG", True)

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./sql_app.db")
DLIB_MODEL_PATH = os.environ.get(
    "DLIB_SHAPE_PREDICTOR", "shape_predictor_5_face_landmarks.dat"
)
