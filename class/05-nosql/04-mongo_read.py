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

# Get a single document (natural order); may be None if collection is empty
get_one = items.find_one()
print("One document:", dumps(get_one, indent=2))

# Get documents matching a filter (e.g. by name)
get_another = items.find({"name": "apple"})
print(dumps(list(get_another), indent=2))

# Count documents matching a filter
get_more = items.count_documents({"quantity": {"$gte": 5}})
print(get_more, "items with quantity >= 5")

# Close the connection
client.close()