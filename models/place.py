#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

hbnb_storage = getenv('HBNB_TYPE_STORAGE', default=None)
place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


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

    amenities = relationship('Amenity', secondary=place_amenity,
                             back_populates='place_amenities', viewonly=False)

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

        @property
        def amenities(self):
            """returns the list of Amenity instances based on the attribute \
amenity_ids that contains all Amenity.id linked to the Place
            """
            from amenity import Amenity
            from __init__ import storage

            amenity_objs = storage.all(Amenity)
            collection = []
            for amenity_id in self.amenity_ids:
                for obj in amenity_objs:
                    if obj.id == amenity_id:
                        collection.append(obj)
            return collection

        @property.setter
        def amenities(self, obj):
            """ handles append method for adding an Amenity.id to the attribute amenity_ids"""
            from amenity import Amenity

            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
