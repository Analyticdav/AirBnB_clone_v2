#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

hbnb_storage = getenv('HBNB_TYPE_STORAGE', default=None)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'))
    user_id = Column(String(60), ForeignKey('users.id'))
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    reviews = relationship('Review', backref='place',
                           cascade='all, delete-orphan')

    if hbnb_storage != 'db':
        @property
        def reviews(self):
            """returns review objects with place_id == self.id"""
            from review import Review
            from __init__ import storage
            
            review_objs = storage.all(Review)
            review_list = []
            for review in review_objs.values():
                if review.place_id == self.id:
                    review_list.append(review)
