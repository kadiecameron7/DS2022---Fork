"""Shared Atlas connection for the mypractice exercises (scripts 02+)."""
import os
from pymongo import MongoClient

uri = os.getenv("MONGODB_ATLAS_URL")
username = os.getenv("MONGODB_ATLAS_USER")
password = os.getenv("MONGODB_ATLAS_PWD")

client = MongoClient(
    uri,
    username=username,
    password=password,
    connectTimeoutMS=200,
    retryWrites=True,
)
db = client.mypractice
fruit = db.fruit
