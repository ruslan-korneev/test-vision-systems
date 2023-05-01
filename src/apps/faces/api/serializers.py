from src.apps.faces.models import Face, Image, Landmark
from src.config.settings import ma


class LandmarkSchema(ma.Schema):
    class Meta:
        model = Landmark


class FaceSchema(ma.Schema):
    landmarks = ma.Nested("LandmarkSchema", many=True)

    class Meta:
        model = Face


class ImageSchema(ma.Schema):
    faces = ma.Nested(FaceSchema, many=True)

    class Meta:
        model = Image
