import pandas
import twint
import os
import requests
from datetime import datetime
from mongo_db import MongoDB
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta
from mongo_db import MongoDB

class DataCollector:
    def fetchFearAndGreedIndex(self) -> None:
        resp = requests.get(os.environ.get("FEAR_AND_GREED_URL"))
        mongoDb = MongoDB(os.environ.get("FEAR_AND_GREED_COLLECTION"))

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
        
        
    def fetchPrice(self, ticker: str) -> None:
        client = MongoDB('{}_price_snapshots'.format(ticker))
        uri_ticker_price = 'https://api.binance.com/api/v3/ticker/price?symbol={}USDT'.format(ticker.upper())
        data_price = requests.get(uri_ticker_price)  
        data_price = data_price.json()
        
        uri_ticker_volume = 'https://api.binance.com/api/v3/ticker/24hr?symbol={}USDT'.format(ticker.upper())
        data_volume = requests.get(uri_ticker_volume)  
        data_volume = data_volume.json()

        mongoDbObject = {
            'created_at': datetime.now().timestamp(),
            'price': data_price['price'],
            **data_volume
        }
                
        client.collection.insert_one(mongoDbObject)
        print("Successfully inserted {} price data".format(ticker))
    
    def analyzeTweet(self, tweet: dict) -> dict:
        analyzer = SentimentIntensityAnalyzer()
    
        sentiment_result = analyzer.polarity_scores(tweet['tweet'])
        tweet['sentiment_dict'] = sentiment_result
            
        if sentiment_result['compound'] >= 0.05:
            tweet['sentiment'] = "pos"
        elif sentiment_result['compound'] <= -0.05:
            tweet['sentiment'] = "neg"
        else:
            tweet['sentiment'] = "neu"
            
        return tweet
    
    def fetchTweets(self, query: str, coin: str) -> None:
        print('Fetching tweets for query {}'.format(query))
        time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
        print(time.strftime("%Y-%m-%d %H:%M:%S"))
        config = twint.Config()
        config.Search = query
        config.Since = time.strftime("%Y-%m-%d %H:%M:%S")
        config.User_full = True
        config.Hide_output = True
        config.Count = True
        config.Pandas = True
            
        try: 
            twint.run.Search(config)
            
            tweets_df: pandas.DataFrame = twint.storage.panda.Tweets_df
            tweets_clean = tweets_df.drop(columns=["id", "conversation_id", "timezone", "place", "day", "hour", "link", "quote_url", "near", "geo", "source"])       
            mongoDb = MongoDB(coin)
            tweets = tweets_clean.to_dict(orient="records")
            
            for tweet in tweets:
                tweet = self.analyzeTweet(tweet)
            
            mongoDb.collection.insert_many(tweets)
            print("Successfully uploaded tweets")

        except Exception as e:
            print(e)