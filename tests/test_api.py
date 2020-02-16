"""TEST API
Test on the real deployed API using a real MongoDB server (nothing mocked/patched).
"""

# # Native # #
import json
import multiprocessing
import time
import random

# # Installed # #
import requests
import pytest
from starlette import status as statuscode
from pymongo import MongoClient

# # Project # #
from busbot_data_manager.app import run
from busbot_data_manager.settings_handler import settings
from busbot_data_manager.entities import *

# TODO Update stop_id, user_id, stop_name kwargs
class TestAPI:
    mongo_client = None
    mongo_collection = None
    initial_stops = [
        SavedStop(user_id=1, stop_id=1),
        SavedStop(user_id=1, stop_id=2, name="Stop 2"),
        SavedStop(user_id=2, stop_id=1)
    ]
    inserted_stops = list()  # (userid, stopid)
    stops_timestamps = list()
    api_url = "http://localhost:" + str(settings.port)
    api_process = multiprocessing.Process(target=run, daemon=True)

    def __insert_stop(self, d):
        now = int(time.time())
        self.mongo_collection.insert_one(d)
        self.stops_timestamps.append(now)
        self.inserted_stops.append((d["user_id"], d["stop_id"]))

    def __find_stop(self, user_id, stop_id):
        return self.mongo_collection.find_one({"stop_id": stop_id, "user_id": user_id})

    @staticmethod
    def __approx_timestamp(timestamp):
        return pytest.approx(timestamp, 1)

    def setup_class(self):
        self.api_process.start()
        time.sleep(3)  # TODO RM/Alternative
        self.mongo_client = MongoClient(settings.mongo_uri)
        self.mongo_collection = self.mongo_client[settings.mongo_stops_db][settings.mongo_stops_collection]

    def setup_method(self):
        for stop in self.initial_stops:
            self.__insert_stop(stop.get_mongo_dict())

    def teardown_method(self):
        for userid, stopid in self.inserted_stops:
            self.mongo_collection.delete_one(filter={
                "stopid": stopid,
                "userid": userid
            })
        self.stops_timestamps.clear()

    def test_api_status(self):
        r = requests.get(self.api_url + "/status")
        assert r.status_code == 200

    def test_get_stops(self):
        # Get saved stops of user 1
        r = requests.get(self.api_url + "/stops/1")
        assert r.status_code == statuscode.HTTP_200_OK

        result = json.loads(r.text)
        assert len(result) == 2

        result.sort(key=lambda d: d["stopid"])

        assert result[0] == {
            "stopid": 1,
            "created": self.__approx_timestamp(self.stops_timestamps[0]),
            "updated": self.__approx_timestamp(self.stops_timestamps[0])
        }

        assert result[1] == {
            "stopid": 2,
            "name": "Stop 2",
            "created": self.__approx_timestamp(self.stops_timestamps[1]),
            "updated": self.__approx_timestamp(self.stops_timestamps[1])
        }

    def test_insert_stop(self):
        stopid = random.randint(10, 10000)
        userid = random.randint(10, 10000)
        name = "My Custom Stop Name"

        body = {
            "stopid": stopid,
            "userid": userid,
            "name": name
        }

        r = requests.post(
            url=self.api_url + "/stops",
            json=body
        )
        inserted_timestamp = self.__approx_timestamp(int(time.time()))

        assert r.status_code == statuscode.HTTP_201_CREATED

        inserted_document = self.__find_stop(userid, stopid)
        assert inserted_document["created"] == inserted_timestamp
        assert inserted_document["updated"] == inserted_timestamp
        assert inserted_document["stopid"] == stopid
        assert inserted_document["userid"] == userid
        assert inserted_document["name"] == name

    def test_insert_stop_document_id(self):
        stopid = 2
        userid = 3
        # _id = md5; update w/ userid; update w/ stopid
        document_id = "6364d3f0f495b6ab9dcf8d3b5c6e0b01"

        body = {
            "stopid": stopid,
            "userid": userid
        }

        requests.post(
            url=self.api_url + "/stops",
            json=body
        )

        inserted_document = self.__find_stop(userid, stopid)
        assert inserted_document["_id"] == document_id

    def test_insert_string_user_stop(self):
        stopid = "j2h289sjs"
        userid = "kk2878sjk"

        body = {
            "stopid": stopid,
            "userid": userid
        }

        requests.post(
            url=self.api_url + "/stops",
            json=body
        )

        inserted_document = self.__find_stop(userid, stopid)
        assert inserted_document["stopid"] == stopid
        assert inserted_document["userid"] == userid
