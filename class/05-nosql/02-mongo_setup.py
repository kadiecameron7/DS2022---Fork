#!/usr/bin/env python3

from pymongo import MongoClient, errors
import os
# Use the shared client from database.py (same connection, mypractice db and items collection)
from database import client, db, items

# Connection and database info (mypractice db from mongosh practice)
print("Server:", client.server_info().get("version", "?"))

dbs = client.list_database_names()
print("Databases:", dbs)

colls = db.list_collection_names()
print("Collections in mypractice:", colls)

count = items.count_documents({})
print(count, "items")
many = items.count_documents({"quantity": {"$gte": 5}})
print(many, "items with quantity >= 5")

# Close the connection
client.close()