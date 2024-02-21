#!/usr/bin/python3
"""defined User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """User class"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes User class"""
        super().__init__(*args, **kwargs)
