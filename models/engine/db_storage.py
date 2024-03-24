#!/usr/bin/python3
"""Database Storage engine"""
import os
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

data_cls = {
    'Amenity': Amenity,
    'State': State,
    'City': City,
    'Review': Review,
    'User': User,
    'Place': Place
}


class DB_storage:
    """Database Storage class"""
    __engine = None
    __session = None
    
    def __init__(self):
        """initializes the db_storage"""
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        user = os.getenv('HBNB_MYSQL_USER')
        database = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, database))
        
        try:
            if os.environ['HBNB_MYSQL_ENV'] == "test":
                Base.metadata.drop_all(self.__engine)
        except KeyError:
            pass
        
    def all(self, cls=None):
        """Query on current database session"""    
        if not self.__session:
            self.reload()
            
        objects = {}
        
        if isinstance(cls, str):
            cls = data_cls.get(cls, None)
        if cls:
            query_result = self.__session.query(cls).all()
        else:
            query_result = [obj for cls in data_cls.values() for obj in self.__session.query(cls).all()]
            
        for obj in query_result:
            objects[f"{obj.__class__.__name__}.{obj.id}"] = obj
            
        return objects
    
    def new(self, obj):
        """creates new object, adds to current db session"""
        self.__session.add(obj)
    
    def save(self):
        """commits all changes to current db session"""
        self.__session.commit()
    
    def delete(self, obj=None):
        """delete from current db session obj if not None"""
        if not self.__session:
            self.reload()
        if obj is not None:
            self.__session.delete(obj)
    
    def reload(self):
        """reloads all tables in db"""
        session_fctry = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_fctry)
