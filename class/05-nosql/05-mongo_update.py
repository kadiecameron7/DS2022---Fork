#!/usr/bin/env python3
"""Update mypractice.fruit (targets differ from the mongosh apple / updateMany examples)."""
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

log.info("Before update:")
log.info("%s", dumps(list(fruit.find({})), indent=2))

# Distinct from mongosh (which updates apple and uses updateMany on quantity < 10)
fruit.update_one({"name": "banana"}, {"$set": {"quantity": 12}})
fruit.update_one({"name": "orange"}, {"$set": {"restocked": True}})

# Full list of MongoDB operators: https://www.mongodb.com/docs/manual/reference/operator/

log.info("After update:")
log.info("%s", dumps(list(fruit.find({})), indent=2))

client.close()
