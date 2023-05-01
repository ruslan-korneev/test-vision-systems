from pydantic import ValidationError

ALLOWED_EXTENSIONS = {"jpg", "jpeg"}


def validated_image(image):
    if not image:
        raise ValidationError("Image is required")

    if image.filename not in ALLOWED_EXTENSIONS:
        raise ValidationError("Image extension is not allowed")

    return image
