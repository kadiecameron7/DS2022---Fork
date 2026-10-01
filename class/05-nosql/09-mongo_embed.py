#!/usr/bin/env python3
"""Embed comments into a movie document and save it in mypractice."""
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
mflix = client.sample_mflix
practice = client.mypractice

# Start from the movie; $lookup embeds matching comments as an array
pipeline = [
    {"$match": {"title": "The Godfather"}},
    {
        "$lookup": {
            "from": "comments",
            "localField": "_id",
            "foreignField": "movie_id",
            "as": "comments",
        }
    },
    {
        "$project": {
            "title": 1,
            "year": 1,
            "comments.name": 1,
            "comments.text": 1,
        }
    },
]
doc = next(mflix.movies.aggregate(pipeline))
log.info("Movie with embedded comments:\n%s", dumps(doc, indent=2))

# Store the new shape in mypractice (creates the collection on insert)
result = practice.movies_with_comments.insert_one(doc)
log.info("Inserted into mypractice.movies_with_comments with _id=%s", result.inserted_id)

saved = practice.movies_with_comments.find_one({"_id": result.inserted_id})
log.info("Saved document:\n%s", dumps(saved, indent=2))

client.close()
