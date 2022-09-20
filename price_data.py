from datetime import datetime
import requests
from mongo_db import MongoDB
from dotenv import load_dotenv
load_dotenv()
import os
import schedule
import time

lrc_ticker = os.environ.get("LRC_TICKER")
stx_ticker = os.environ.get("STX_TICKER")
mongo_db_uri = os.environ.get("MONGO_DB_URI")
mongo_db_table = os.environ.get("MONGO_DB_TABLE")

def fetchPrice(ticker: str) -> None:
    client = MongoDB('{}_price_snapshots'.format(ticker))
    key = 'https://api.binance.com/api/v3/ticker/price?symbol={}USDT'.format(ticker.upper())
    data = requests.get(key)  
    data = data.json()

    mongoDbObject = {
        'created_at': datetime.now().timestamp(),
        'price': data['price']
    }
    
    client.collection.insert_one(mongoDbObject)
    print("Successfully inserted {} price data".format(ticker))
    
schedule.every(30).minutes.do(lambda: fetchPrice(lrc_ticker))
schedule.every(30).minutes.do(lambda: fetchPrice(stx_ticker))

while True:
    schedule.run_pending()
    time.sleep(1)