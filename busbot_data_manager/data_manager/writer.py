"""WRITER
Write data (insert, modify or delete) on MongoDB
"""

# # Project # #
from ..entities import *

# # Package # #
from .mongo import fake_database

__all__ = ("save_stop", "modify_stop", "delete_stop")


def save_stop(stop: SavedStop):
    # TODO use real MongoDB
    # TODO Check that Stop is not saved - Generate _id based on StopID AND User?
    fake_database.append(stop)


def modify_stop(userid: int, stopid: int, new_stop: SavedStop):
    # TODO use real MongoDB
    delete_stop(userid, stopid)
    fake_database.append(new_stop)


def delete_stop(userid: int, stopid: int):
    # TODO use real MongoDB
    fake_database.remove(next(s for s in fake_database if s.user == userid and s.stopid == stopid))
