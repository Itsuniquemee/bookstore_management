from pymongo import MongoClient
from config import DATABASE_URI, DATABASE_NAME

def get_db():
    client = MongoClient(DATABASE_URI)
    return client[DATABASE_NAME]
