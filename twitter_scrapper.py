import pandas
import twint
from datetime import datetime, timedelta
from mongo_db import MongoDB
from sentiment_analysis import analyzeTweet
import schedule
import time

def getTweets(query: str, coin: str) -> None:
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
            tweet = analyzeTweet(tweet)
        
        mongoDb.collection.insert_many(tweets)
        print("Successfully uploaded tweets")

    except Exception as e:
        print(e)
        
schedule.every().monday.at("00:00").do(lambda: getTweets('$stx OR #stx', 'stacks'))
schedule.every().monday.at("00:00").do(lambda: getTweets('$lrc OR #lrc', 'loopring'))

while True:
    schedule.run_pending()
    time.sleep(1)
