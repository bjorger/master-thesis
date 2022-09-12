from datetime import datetime
import requests
from mongo_db import MongoDB
from dotenv import load_dotenv
load_dotenv()
import os
from pymongo import MongoClient

lrc_ticker = os.environ.get("LRC_TICKER")
stx_ticker = os.environ.get("STX_TICKER")
mongo_db_uri = os.environ.get("MONGO_DB_URI")
mongo_db_table = os.environ.get("MONGO_DB_TABLE")

def fetchPrice(ticker: str) -> None:
    client = MongoClient(mongo_db_uri)
    db = client[mongo_db_table]
    mongoDb = db['tweets.{}'.format('{}_price_snapshots').format(ticker)]
    key = 'https://api.binance.com/api/v3/ticker/price?symbol={}USDT'.format(ticker.upper())
    data = requests.get(key)  
    data = data.json()

    mongoDbObject = {
        'created_at': datetime.now().timestamp(),
        'price': data['price']
    }
    
    mongoDb.insert_one(mongoDbObject)
    
fetchPrice(lrc_ticker)
fetchPrice(stx_ticker)