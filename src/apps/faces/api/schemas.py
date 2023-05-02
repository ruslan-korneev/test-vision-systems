from src.apps.faces.models import Face, Image, Landmark
from src.config.settings import ma


class LandmarkSchema(ma.Schema):
    class Meta:
        model = Landmark
        fields = ("x", "y")


class FaceSchema(ma.Schema):
    landmarks = ma.Nested("LandmarkSchema", many=True)

    class Meta:
        model = Face
        fields = ("left", "top", "right", "bottom", "landmarks")
