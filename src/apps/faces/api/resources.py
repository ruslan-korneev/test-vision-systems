from flask import request
from flask_restful import Resource
from pydantic import ValidationError

from src.apps.base.api.serializers import ImageUploadSchema
from src.apps.faces.api.serializers import FaceSchema
from src.apps.faces.api.validations import validated_image
from src.apps.faces.models import Image
from src.apps.faces.services import detect_faces
from src.database.config import Session


class FaceDetection(Resource):
    def post(self):
        try:
            image = request.files["image"]
            validated_image(image)
        except ValidationError as e:
            return e.errors(), 400

        faces = detect_faces(image)
        image_instance = Image(image=image.read())
        image_instance.faces = faces
        session = Session()
        session.add(image_instance)
        session.commit()

        schema = FaceSchema(many=True)
        return schema.dump(image_instance.faces), 200


class FaceComparison(Resource):
    def post(self):
        try:
            image = request.files["image"]
            ImageUploadSchema(image=image.read())
        except ValidationError as e:
            return e.errors(), 400

        return {"message": "Face comparison"}, 201
