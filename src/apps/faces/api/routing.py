from flask import Blueprint
from flask_restful import Api

from src.apps.faces.api.resources import FaceDetection, FaceComparison

api_face = Blueprint("face", __name__)
api = Api(api_face, prefix="/api/v1/face")

api.add_resource(FaceDetection, "/detection", endpoint="face-detection")
api.add_resource(FaceComparison, "/comparison", endpoint="face-comparison")
