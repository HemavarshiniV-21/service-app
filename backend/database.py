from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    # Test connection
    client.admin.command('ping')
    db = client["vehicle_service"]
    print("MongoDB connected successfully")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    db = None
    client = None

# Collections
if db is not None:
    users_collection = db["users"]
    chat_history_collection = db["chat_history"]
    vehicle_issues_collection = db["vehicle_issues"]
    service_requests_collection = db["service_requests"]
else:
    users_collection = None
    chat_history_collection = None
    vehicle_issues_collection = None
    service_requests_collection = None