from flask_restful import Resource, reqparse
from marshmallow import ValidationError
from werkzeug.datastructures import FileStorage

from src.apps.faces.api.schemas import FaceSchema
from src.apps.faces.api.validations import validated_image
from src.apps.faces.models import Image
from src.apps.faces.services import detect_faces, count_matching_faces
from src.database.config import Session


class FaceDetection(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("image", type=FileStorage, location="files")

    def post(self):
        args = self.parser.parse_args()
        image = args["image"]
        try:
            validated_image(image)
        except ValidationError as e:
            return e.messages_dict, 400

        image_instance = Image(filename=image.filename, image=image.read())
        image_instance = detect_faces(image_instance)
        session = Session()
        session.add(image_instance)
        session.commit()

        data = self.get_data(image_instance)
        return data, 200
        # return schema.dump(image_instance.faces, many=True), 200

    def get_data(self, image_instance: Image) -> dict | list[dict]:
        schema = FaceSchema()
        return schema.dump(image_instance.faces, many=True)


class FaceComparison(FaceDetection):
    def get_data(self, image_instance: Image) -> dict | list[dict]:
        return {
            "faces": image_instance.faces.count(),
            "matching_faces": count_matching_faces(image_instance),
        }
