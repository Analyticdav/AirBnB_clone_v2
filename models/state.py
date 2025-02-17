#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

hbnb_storage = getenv('HBNB_TYPE_STORAGE', default=None)


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state',
                          cascade='all, delete-orphan')

    if hbnb_storage != 'db':
        @property
        def cities(self):
            """
            Getter for cities associated with state
            """
            from models.city import City
            from models import storage
            city_objs = [value for value in storage.all(City).values()
                         if value.state_id == self.id]
            return city_objs
