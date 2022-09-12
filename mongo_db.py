import os
from pymongo import MongoClient, cursor
from dotenv import load_dotenv
load_dotenv()
import os

mongo_db_uri = os.environ.get("MONGO_DB_URI")
mongo_db_table = os.environ.get("MONGO_DB_TABLE")

class MongoDB: 
    client = MongoClient(mongo_db_uri)
    db = client[mongo_db_table]
    collection = None
    
    def __init__(self, collection_name: str) -> None:
        self.collection = self.db['tweets.{}'.format(collection_name)]
