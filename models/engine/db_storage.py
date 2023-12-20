#!/usr/bin/python3
"""
Contains the definition for the DBStorage class
"""
from os import getenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """\
Engine that handles storage to a mysql database
    """
    __engine = None
    __session = None

    __env = {
            'user': getenv('HBNB_MYSQL_USER', default=None),
            'password': getenv('HBNB_MYSQL_PWD', default=None),
            'host': getenv('HBNB_MYSQL_HOST', default='localhost'),
            'database': getenv('HBNB_MYSQL_DB', default=None),
            'env': getenv('HBNB_ENV', default=None)
    }

    __types = {
            'State': State, 'City': City, 'User': User, 'Place': Place,
            'Review': Review, 'Amenity': Amenity
    }

    def __init__(self):
        """Initializes an instance of the class"""
        env = self.__env
        url = URL.create(
                'mysql+mysqldb',
                username=env['user'],
                password=env['password'],
                host=env['host'],
                database=env['database']
        )
        self.__engine = create_engine(url, pool_pre_ping=True)
        if env['env'] == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary of objects depending of the class name: cls"""
        objects = {}
        if cls:
            cls_objects = self.__session.query(cls).all()
            for cls_object in cls_objects:
                key = "{}.{}".format(cls.__name__, cls_object.id)
                objects[key] = cls_object
        else:
            for key, val in self.__types.items():
                cls_objects = self.__session.query(val).all()
                for cls_object in cls_objects:
                    key = "{}.{}".format(key, cls_object.id)
                    objects[key] = cls_object
        return objects

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database and create the current \
database session
        """
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()
