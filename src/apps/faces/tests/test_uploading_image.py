# import pytest


# TODO: @pytest.mark.flask_db
def test_uploading_image(client):
    response = client.post(
        "/api/v1/face/detection",
        data={"image": (open("tests/data/face.jpg", "rb"), "face.jpg")},
    )
    assert response.status_code == 201
    assert response.json == {"message": "Face detection"}


# TODO: @pytest.mark.flask_db
def test_uploading_image_wrong_extension(client):
    response = client.post(
        "/api/v1/face/detection",
        data={"image": (open("tests/data/face.txt", "rb"), "face.txt")},
    )
    assert response.status_code == 400
    assert response.json == {
        "image": [
            {
                "loc": ["image"],
                "msg": "The file extension must be one of the following types: jpg, jpeg.",
                "type": "value_error",
            }
        ]
    }
