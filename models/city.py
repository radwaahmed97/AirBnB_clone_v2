#!/usr/bin/python3
"""contains City class"""

from models.base_model import BaseModel


class City(BaseModel):
    """City class"""

    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """initializes city class"""
        super().__init__(*args, **kwargs)
