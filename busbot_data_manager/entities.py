"""ENTITIES
Definition of custom classes
"""

# # Native # #
import copy
from typing import Optional

# # Installed # #
# noinspection PyProtectedMember
from pybusent.entities import BaseEntity

__all__ = ("SavedStop",)


class SavedStop(BaseEntity):
    # TODO Different entities for internal (Mongo), input (POST/PATCH) and output (GET) objects
    """A Stop saved by a User.
    """
    user: int
    stopid: int
    name: Optional[str]

    def get_api_dict(self):
        """Like get_dict but removing unwanted fields to return by the API: user"""
        d = copy.deepcopy(self.get_dict())
        d.pop("user")
        return d
