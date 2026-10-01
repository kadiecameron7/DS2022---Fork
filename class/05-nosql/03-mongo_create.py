#!/usr/bin/env python3
"""Create mypractice / fruit and insert sample documents."""
import logging
import os

from bson.json_util import dumps
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

uri = os.getenv("MONGODB_ATLAS_URL")
username = os.getenv("MONGODB_ATLAS_USER")
password = os.getenv("MONGODB_ATLAS_PWD")

client = MongoClient(uri, username=username, password=password, connectTimeoutMS=200, retryWrites=True)
db = client.mypractice
fruit = db.fruit

new_record = {"name": "apple", "quantity": 5}
fruit.insert_one(new_record)
fruit.insert_many([{"name": "banana", "quantity": 10}, {"name": "orange", "quantity": 3}])

get_records = fruit.find()
log.info("%s", dumps(list(get_records), indent=2))

client.close()
