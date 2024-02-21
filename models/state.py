#!/usr/bin/env python3
"""contains State class"""

from models.base_model import BaseModel


class State(BaseModel):
    """State class"""

    name = ""

    def __init__(self, *args, **kwargs):
        """initializes state class"""
        super().__init__(*args, **kwargs)
