#!/usr/bin/python3
"""BaseModel class defines common attributes and methods for other classes"""

from sqlalchemy.ext.declarative import declarative_base
import uuid
import models
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime


Base = declarative_base()


class BaseModel:
    """BaseModel class"""

    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))

    def __init__(self, *args, **kwargs):
        """initializes of the BaseModel class."""

        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """BaseModel class string representation"""
        imaginary = self.__class__.__name__
        return f"[{str(imaginary)}] ({str(self.id)}) {self.__dict__}"

    def __repr__(self):
        """return a string representaion
        """
        return self.__str__()

    def save(self):
        """
        updates the BaseModel's attribute 'updated_at'
        with the current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary containing
        all keys/values of __dict__ of the instance
        """
        new_dict = dict(self.__dict__)
        new_dict["__class__"] = str(type(self).__name__)
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        if '_sa_instance_state' in new_dict.keys():
            del new_dict['_sa_instance_state']
        return new_dict

    def delete(self):
        """ delete object
        """
        models.storage.delete(self)
