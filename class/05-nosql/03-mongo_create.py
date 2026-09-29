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

# Simple document structure matching mongosh practice: name, quantity
new_record = {"name": "apple", "quantity": 5}

# Insert a single record
items.insert_one(new_record)

# Insert multiple records
items.insert_many([{"name": "banana", "quantity": 10}, {"name": "orange", "quantity": 3}])

# Get all records
get_records = items.find()
print(dumps(list(get_records), indent=2))

# Close the connection
client.close()

