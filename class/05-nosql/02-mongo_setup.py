#!/usr/bin/env python3
"""Connection and mypractice database info (shared client from database.py)."""
import logging

from database import client, db, fruit

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

log.info("Server: %s", client.server_info().get("version", "?"))
log.info("Databases: %s", client.list_database_names())
log.info("Collections in mypractice: %s", db.list_collection_names())

count = fruit.count_documents({})
log.info("%s fruit documents", count)

many = fruit.count_documents({"quantity": {"$gte": 5}})
log.info("%s fruit with quantity >= 5", many)

client.close()
