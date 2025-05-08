import os

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

# MongoDB connection settings
MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME", "future_furniture_db")

# Collections
USERS_COLLECTION = "users"
DESIGNS_COLLECTION = "designs"

# Create a MongoDB client
client = MongoClient(MONGO_URI)
db: Database = client[DB_NAME]

# Get collections
users_collection: Collection = db[USERS_COLLECTION]
designs_collection: Collection = db[DESIGNS_COLLECTION]

# Create indexes
users_collection.create_index("username", unique=True)
designs_collection.create_index("ownerId")
