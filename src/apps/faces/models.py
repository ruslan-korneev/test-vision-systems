from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship

from src.config.settings import db


class Landmark(db.Model):
    __tablename__ = "landmarks"

    id = Column(Integer, primary_key=True)
    face_id = Column(Integer, ForeignKey("faces.id"), nullable=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)


class Face(db.Model):
    __tablename__ = "faces"

    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=True)
    top = Column(Integer, nullable=False)
    bottom = Column(Integer, nullable=False)
    left = Column(Integer, nullable=False)
    right = Column(Integer, nullable=False)
    landmarks = relationship("Landmark", backref="face", lazy="dynamic")


class Image(db.Model):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    filename = Column(db.String(255), nullable=False)
    image = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    faces = relationship("Face", backref="image", lazy="dynamic")
