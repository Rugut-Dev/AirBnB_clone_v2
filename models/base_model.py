#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
    
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    
    
    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for k, v in kwargs.items():
                if k == '__class__':
                    continue
                setattr(self, k, v)
                if isinstance(self.created_at, str):
                    self.created_at = datetime.strptime(self.created_at, 
                                                        '%Y-%m-%dT%H:%M:%S.%f')
                if isinstance(self.updated_at, str):
                    self.created_at = datetime.strptime(self.created_at, 
                                                        '%Y-%m-%dT%H:%M:%S.%f')

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_to_disk=False):
        """Returns a dictionary containing all keys/values of the instance"""
        new_dict = {
            key: value.isoformat() if isinstance(value, datetime) else value
            for key, value in self.__dict__.items()
            if key not in ['amenities', 'reviews', '_sa_instance_state']
        }
        
        if '_password' in new_dict:
            new_dict['password'] = new_dict.pop('_password')
            
        new_dict["__class__"] = self.__class__.__name__
        
        if not save_to_disk:
            new_dict.pop('password', None)
            
        return new_dict
    
    def delete(self):
        """Delete current instance from the storage"""
        models.storage.delete(self)
        
    
