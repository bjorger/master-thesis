import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os

mongo_db_uri = os.environ.get("MONGO_DB_URI")

class MongoDB: 
    client = MongoClient(mongo_db_uri)
    db = client.Masterprojekt

    def storeTweets(self, tweets_to_store: dict, coin: str):
        tweets = self.db['tweets.{}'.format(coin)]
        tweets.insert_many(tweets_to_store.to_dict(orient="records"))
        
    def fetchTweets(self, coin):
        table = self.db['tweets.{}'.format(coin)]
        tweets = table.find()
        
        for tweet in tweets:
            print(tweet)
        

