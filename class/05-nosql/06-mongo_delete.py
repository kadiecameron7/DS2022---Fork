#!/usr/bin/env python3

from pymongo import MongoClient, errors
from bson.json_util import dumps
import pprint
import os

# Use environment variables from README: MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD
uri = os.getenv('MONGODB_ATLAS_URL')
username = os.getenv('MONGODB_ATLAS_USER')
password = os.getenv('MONGODB_ATLAS_PWD')

client = MongoClient(uri, username=username, password=password, connectTimeoutMS=200, retryWrites=True)
db = client.mypractice
items = db.items

# Show items before delete
get_record = items.find({"name": "orange"})
print("Before delete:", dumps(list(get_record), indent=2))

# Deletes first document matching criteria
items.delete_one({"name": "orange"})

# Show remaining items
get_record = items.find({})
print("After delete:", dumps(list(get_record), indent=2))

# To delete all documents matching a filter: items.delete_many({"name": "orange"})

# Close the connection
client.close()