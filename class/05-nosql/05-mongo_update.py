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

# Update one document - set new quantity for "apple" using $set
items.update_one({"name": "apple"}, {"$set": {"quantity": 8}})

# Add an optional field with $set
items.update_one({"name": "apple"}, {"$set": {"restocked": True}})

# The full list of MongoDB operators: https://www.mongodb.com/docs/manual/reference/operator/

get_record = items.find({"name": "apple"})
print(dumps(list(get_record), indent=2))

# Close the connection
client.close()