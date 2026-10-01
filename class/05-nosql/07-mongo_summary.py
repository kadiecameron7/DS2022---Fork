#!/usr/bin/env python3
"""Log a summary of mypractice after the fruit CRUD scripts (03–06)."""
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

log.info("Server: %s", client.server_info().get("version", "?"))
log.info("Collections in mypractice: %s", db.list_collection_names())
log.info("Total fruit documents: %s", fruit.count_documents({}))
log.info("All fruit documents:\n%s", dumps(list(fruit.find({})), indent=2))

client.close()
