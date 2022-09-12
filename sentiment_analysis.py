from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient

def getTweets(coin: str): 
    client = MongoClient("")
    db = client.Masterprojekt
    tweets = db['tweets.{}'.format(coin)]
    tweets_ = tweets.find()
    
    for tweet in tweets_:
        print(tweet)
        
getTweets("loopring")