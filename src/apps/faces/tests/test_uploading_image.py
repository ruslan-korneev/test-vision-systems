# TODO: resolve issue with calling endpoints: not found endpoints
import io

import pytest


@pytest.fixture()
def image(request):
    image = open(f"src/apps/faces/tests/data/{request.param}", "rb")
    yield io.BytesIO(image.read())
    image.close()


@pytest.mark.skip
@pytest.mark.parametrize("image", ["faces.jpg"], indirect=True)
def test_uploading_image(image, client):
    response = client.post("/api/v1/face/detection", data={"image": image})
    assert response.status_code == 201


@pytest.mark.skip
@pytest.mark.parametrize("image", ["faces.txt"], indirect=True)
def test_uploading_image_wrong_extension(image, client):
    response = client.post("/api/v1/face/detection", data={"image": image})
    assert response.status_code == 400, response.data
