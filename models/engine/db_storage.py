#!/usr/bin/python3
""" This modules handles Database Storage """
from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.amenity import Amenity


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

class DBStorage:
    '''
    DBStorage
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''create engine'''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True
        )
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for childCls in classes:
            if cls is None or cls is classes[childCls] or cls is childCls:
                objs = self.__session.query(classes[childCls]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        '''add the object to the current database session'''
        self.__session.add(obj)

    def save(self):
        '''commit all changes of the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete obj from the current database session'''
        self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Because SQLAlchemy doesn't reload his `Session`
        when it's time to insert new data, we force it to!
        """
        self.__session.close()
