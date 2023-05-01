from flask import Flask

from src.apps.faces.api.routing import api_face
from src.config import settings

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
app.register_blueprint(api_face)


def main():
    app.run(debug=settings.DEBUG)


if __name__ == "__main__":
    main()
