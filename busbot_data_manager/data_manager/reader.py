"""READER
Read data from MongoDB
"""

# # Native # #
from typing import List

# # Project # #
from ..entities import *

# # Package # #
from .mongo import fake_database

__all__ = ("get_user_stops",)


def get_user_stops(userid: int) -> List[SavedStop]:
    # TODO use real MongoDB
    return [s for s in fake_database if s.user == userid]
