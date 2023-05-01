from pydantic import BaseModel


class DetectedFaceSchema(BaseModel):
    class Meta:
        fields = ("bounding_box", "landmarks")
