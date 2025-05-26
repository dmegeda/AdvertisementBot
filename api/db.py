import os
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "ads_db")

client: MongoClient = MongoClient(MONGO_URI)
db: Database = client[DB_NAME]

posts_collection: Collection[dict[str, Any]] = db.posts
users_collection: Collection[dict[str, Any]] = db.users
categories_collection: Collection[dict[str, Any]]  = db.categories
