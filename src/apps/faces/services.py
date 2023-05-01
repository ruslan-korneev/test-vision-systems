import dlib

from src.apps.faces.models import Face, Landmark
from src.config import settings


def detect_faces(image):
    detector = dlib.get_frontal_face_detector()
    img = dlib.load_rgb_image(image)
    faces = detector(img, 1)
    for face in faces:
        # face_instance = Face(
        #     left=face.left(), top=face.top(), right=face.right(), bottom=face.bottom()
        # )
        predictor = dlib.shape_predictor(settings.DLIB_MODEL_PATH)
        shape = predictor(img, face)
        for index in range(shape.num_parts):
            ...
            # face_instance.landmarks.append(
            #     Landmark(x=shape.part(index).x, y=shape.part(index).y, face=face_instance)
            # )
            # face_instance.save()

    return faces


def compare_faces(self, other):
    # WIP: Compare faces using euclidean distance between landmarks and face coordinates
    # TODO: Calculate it in a database query
    return (
        (self.top - other.top) ** 2
        + (self.bottom - other.bottom) ** 2
        + (self.left - other.left) ** 2
        + (self.right - other.right) ** 2
    ) < 100
