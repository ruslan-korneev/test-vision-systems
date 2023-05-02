# TODO: resolve issue with db.create_all(): not working in tests
import pytest

from src.apps.faces.models import Image, Landmark, Face
from src.apps.faces.services import detect_faces


@pytest.mark.skip
def test_detecting_faces(session):
    with open("src/apps/faces/tests/data/faces.jpg", "rb") as image:
        image_instance = Image(image=image.read(), filename="faces.jpg")
    image_instance = detect_faces(image_instance)
    session = session()
    session.add(image_instance)
    session.commit()
    assert session.query(Image).count() == 1
    assert session.query(Face).count() == 10
    assert session.query(Landmark).count() == 50
