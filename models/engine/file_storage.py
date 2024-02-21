#!/usr/bin/python3
"""FileStorage class"""


import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review,
}


class FileStorage:
    """serializes and deserializes objects to and from a json file."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns a dictionary of __objects"""
        return self.__objects

    def new(self, obj):
        """sets in __objects the object with the given class and id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes all objects to a json file"""
        serialize_dict = {}
        for key in self.__objects.keys():
            serialize_dict[key] = self.__objects[key].to_dict()
        with open(self.__file_path, "w") as f:
            json.dump(serialize_dict, f)

    def reload(self):
        """desrializes all objects from a json file"""
        try:
            with open(self.__file_path, "r", encoding="UTF8") as f:
                deserialize_dict = json.load(f)
            for key, value in deserialize_dict.items():
                self.__objects[key] = classes[value["__class__"]](**value)

        except FileNotFoundError:
            pass
