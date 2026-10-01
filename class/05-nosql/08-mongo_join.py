#!/usr/bin/env python3
"""Join sample_mflix comments to movies via movie_id (manual lookup and $lookup)."""
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
db = client.sample_mflix

# Start from a well-known movie, then find one of its comments
movie = db.movies.find_one({"title": "The Godfather"}, {"title": 1, "year": 1})
log.info("Movie:\n%s", dumps(movie, indent=2))

comment = db.comments.find_one(
    {"movie_id": movie["_id"]},
    {"name": 1, "text": 1, "movie_id": 1},
)
log.info("Comment on that movie:\n%s", dumps(comment, indent=2))

# Manual reference lookup the other way: comment.movie_id -> movies._id
movie_again = db.movies.find_one(
    {"_id": comment["movie_id"]},
    {"title": 1, "year": 1, "_id": 0},
)
log.info("Movie resolved from comment.movie_id:\n%s", dumps(movie_again, indent=2))

# Server-side join: comments for that movie, with $lookup
pipeline = [
    {"$match": {"movie_id": movie["_id"]}},
    {"$limit": 3},
    {
        "$lookup": {
            "from": "movies",
            "localField": "movie_id",
            "foreignField": "_id",
            "as": "movie",
        }
    },
    {
        "$project": {
            "name": 1,
            "text": 1,
            "movie.title": 1,
            "movie.year": 1,
            "_id": 0,
        }
    },
]
joined = list(db.comments.aggregate(pipeline))
log.info("Comments joined to The Godfather ($lookup):\n%s", dumps(joined, indent=2))

client.close()
