from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, LargeBinary
from sqlalchemy.orm import relationship

from src.database.config import Base


class Landmark(Base):
    __tablename__ = "landmarks"

    id = Column(Integer, primary_key=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)


class Face(Base):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True)
    top = Column(Integer, nullable=False)
    bottom = Column(Integer, nullable=False)
    left = Column(Integer, nullable=False)
    right = Column(Integer, nullable=False)
    landmarks = relationship("Landmark", backref="face", lazy="dynamic")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    image = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    faces = relationship("Face", backref="image", lazy="dynamic")
