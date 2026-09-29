#!/usr/bin/env python3
"""Print summary of mypractice db after running scripts 01-06 (collections and item count)."""
import os
from pymongo import MongoClient
from bson.json_util import dumps

uri = os.getenv('MONGODB_ATLAS_URL')
username = os.getenv('MONGODB_ATLAS_USER')
password = os.getenv('MONGODB_ATLAS_PWD')

client = MongoClient(uri, username=username, password=password, connectTimeoutMS=200, retryWrites=True)
db = client.mypractice
items = db.items

print("Server:", client.server_info().get("version", "?"))
print("Collections in mypractice:", db.list_collection_names())
print("Total items:", items.count_documents({}))
print("All items:")
print(dumps(list(items.find({})), indent=2))

client.close()
