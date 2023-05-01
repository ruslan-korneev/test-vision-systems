from pydantic import BaseModel, validator
from magic import Magic


ALLOWED_EXTENSIONS = ("image/jpg", "image/jpeg")


class ImageUploadSchema(BaseModel):
    image: bytes

    @validator("image")
    def validate_image(cls, image):
        if not image:
            raise ValueError("Image is required")

        mime = Magic(mime=True)
        mime_type = mime.from_buffer(image)
        if mime_type not in ALLOWED_EXTENSIONS:
            raise ValueError("File extension not allowed")

        return image
