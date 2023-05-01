from src.database.config import Base
from src.database.config import engine
from src.apps.faces import models as faces_models


def main():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
