"""ENTITIES
Definition of custom classes
"""

# # Native # #
import time
import hashlib
import copy
from typing import Optional, Union, List

# # Installed # #
from pydantic import BaseModel

__all__ = ("SavedStop", "SavedStopList", "UserId", "StopId")

StringInt = Union[int, str]
UserId = StopId = StringInt


class SavedStop(BaseModel):
    """A Stop saved by a User.
    """
    id: Optional[str]
    user_id: UserId
    stop_id: StopId
    stop_name: Optional[str]
    created: Optional[int]
    updated: Optional[int]

    def __init__(self, **kwargs):
        # clear stop_name if not set
        if not kwargs.get("stop_name"):
            kwargs["stop_name"] = None
        super().__init__(**kwargs)

    def get_api_dict(self) -> dict:
        """Like get_dict but removing unwanted fields to return by the API.
        Fields removed: userid, id
        """
        d = copy.deepcopy(self.dict(exclude_none=True))
        d.pop("user_id")
        d.pop("id", None)
        return d

    def get_mongo_dict(self, update: bool = False) -> dict:
        """Like get_dict but adapting the dict to be stored in Mongo.
        - Force generating the custom Document ID.
        - Add timestamps to the object.
        - If update=False, created and updated timestamps are set; if True, only updated timestamp is set.
        - Translate id to _id.
        - Translate null name to empty string.
        """
        self.generate_id()
        self.add_timestamps(created=not update, updated=True)
        d = copy.deepcopy(self.dict(exclude_none=True))
        d["_id"] = d.pop("id")
        if self.stop_name is None:
            d["stop_name"] = ""
        return d

    def get_mongo_update_dict(self):
        """Like get_mongo_dict but adapting the dict to update a existing Mongo document.
        - Returning the document dict with $set as parent, required by Mongo document update method.
        """
        return {
            "$set": self.get_mongo_dict(update=True)
        }

    def get_mongo_filter(self) -> dict:
        """Return the filter to be used to search for a inserted document by Stop ID and User ID.
        The filter searches by the autogenerated ID (based on User ID and Stop ID).
        """
        self.generate_id()
        return {"_id": self.generate_id()}

    def generate_id(self) -> str:
        """Generate a ID, as a md5sum based on the User & Stop. Set to self._id and return it.
        If the Stop already has an ID, return it without regenerating it.
        """
        if self.id:
            return self.id
        md5 = hashlib.md5()
        md5.update(str(self.user_id).encode())
        md5.update(str(self.stop_id).encode())
        new_id = md5.hexdigest()
        self.id = new_id
        return new_id

    def add_timestamps(self, created: bool, updated: bool):
        """Set created/updated timestamps on the object, depending on the created/updated method parameters.
        """
        now = int(time.time())
        if created:
            self.created = now
        if updated:
            self.updated = now


SavedStopList = List[SavedStop]
