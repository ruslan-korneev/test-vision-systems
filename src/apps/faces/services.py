import io
from PIL import Image as PILImage
import dlib
import numpy as np

from src.apps.faces.models import Face, Landmark, Image
from src.config import settings
from src.database.config import Session


def detect_faces(image: Image) -> Image:
    detector = dlib.get_frontal_face_detector()
    pil_image = PILImage.open(io.BytesIO(image.image))
    np_array_img = np.array(pil_image)
    faces = detector(np_array_img, 1)
    for face in faces:
        face_instance = Face(
            left=face.left(), top=face.top(), right=face.right(), bottom=face.bottom()
        )
        predictor = dlib.shape_predictor(settings.DLIB_MODEL_PATH)
        shape = predictor(np_array_img, face)
        for part in shape.parts():
            face_instance.landmarks.append(
                Landmark(x=part.x, y=part.y, face=face_instance)
            )
        image.faces.append(face_instance)

    return image


def count_matching_faces(image: Image) -> int:
    session = Session()
    faces = image.faces.all()
    matching_faces = []
    for face in faces:
        query = (
            session.query(Face)
            .filter(
                Face.image_id != image.id,
                Face.id not in [face.id for face in matching_faces],
            )
            .filter(
                (Face.top - face.top) * (Face.top - face.top)
                + (Face.bottom - face.bottom) * (Face.bottom - face.bottom)
                + (Face.left - face.left) * (Face.left - face.left)
                + (Face.right - face.right) * (Face.right - face.right)
                < 100
            )
        )
        matching_faces.extend(query.all())
    return len(matching_faces)
