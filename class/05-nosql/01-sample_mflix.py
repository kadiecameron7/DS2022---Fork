#!/usr/bin/env python3
"""List sample_mflix collections and document counts."""
import logging
import os

from pymongo import MongoClient

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

uri = os.getenv("MONGODB_ATLAS_URL")
username = os.getenv("MONGODB_ATLAS_USER")
password = os.getenv("MONGODB_ATLAS_PWD")

client = MongoClient(uri, username=username, password=password, connectTimeoutMS=200, retryWrites=True)
db = client.sample_mflix

for name in db.list_collection_names():
    count = db[name].count_documents({})
    log.info("%s: %s documents", name, count)

client.close()
