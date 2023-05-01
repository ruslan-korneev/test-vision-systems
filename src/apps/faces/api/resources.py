from flask import request
from flask_restful import Resource
from pydantic import ValidationError

from src.apps.base.api.serializers import ImageUploadSchema


class FaceDetection(Resource):
    def post(self):
        try:
            image = request.files["image"]
            ImageUploadSchema(image=image.read())
        except ValidationError as e:
            return e.errors(), 400

        faces = detect_faces(image)
        schema = DetectedFaceSchema(faces=faces)
        schema.schema_dict()

        return {"message": "Face detection"}, 201


class FaceComparison(Resource):
    def post(self):
        try:
            image = request.files["image"]
            ImageUploadSchema(image=image.read())
        except ValidationError as e:
            return e.errors(), 400

        return {"message": "Face comparison"}, 201
