from datetime import date, datetime
from xmlrpc.client import DateTime
from dotenv import load_dotenv
from mongo_db import MongoDB
load_dotenv()
import os
import requests
from bs4 import BeautifulSoup
import schedule
import time

fear_and_greed_url = os.environ.get("FEAR_AND_GREED_URL")
fear_and_greed_collection = os.environ.get("FEAR_AND_GREED_COLLECTION")


def fetchFearAndGreedIndex() -> None:
    resp = requests.get(fear_and_greed_url)
    mongoDb = MongoDB(fear_and_greed_collection)

    soup = BeautifulSoup(resp.content, 'html.parser')
    status_element = soup.find('div', 'status')
    status_element_score = soup.find('div', 'fng-circle')
    
    mongoDbObject = {
        'created_at': datetime.now().timestamp(),
        'fear_and_greed': status_element.text,
        'fear_and_greed_score': status_element_score.text
    }
    mongoDb.collection.insert_one(mongoDbObject)
    print("Successfully uplodaded Fear and Greed Index")
    
    
schedule.every().day.at("00:00").do(lambda: fetchFearAndGreedIndex())

while True:
    schedule.run_pending()
    time.sleep(1)