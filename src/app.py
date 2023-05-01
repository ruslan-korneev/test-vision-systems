from src.apps.faces.api.routing import api_face
from src.config import settings
from src.config.settings import app

app.register_blueprint(api_face)


def main():
    app.run(debug=settings.DEBUG)


if __name__ == "__main__":
    main()
