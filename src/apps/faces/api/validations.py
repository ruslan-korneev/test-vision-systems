from marshmallow import ValidationError

ALLOWED_EXTENSIONS = ("jpg", "jpeg")


def validated_image(image):
    if not image:
        raise ValidationError({"image": "Image is required"})

    if image.filename.split(".")[-1] not in ALLOWED_EXTENSIONS:
        raise ValidationError({"image": "Image extension is not allowed"})

    return image
