import pandas
import twint
from pycoingecko import CoinGeckoAPI
from pprint import pprint
from datetime import datetime, timedelta
import schedule
import time
import json
from os import remove
from pymongo import MongoClient

def test():
    print('test')

def getTweets(query: str, coin: str):
    print('Fetching tweets for query {}'.format(query))
    """
        Get time from yesterday at 00:00:00, to fetch all tweets within the last day
    """
    time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    config = twint.Config()
    config.Search = query
    config.Store_csv = True
    config.User_full = True
    config.Output = '{}_output.csv'.format(coin)
    config.Resume = '{}_resume.csv'.format(coin)
    config.Since = time.strftime("%Y-%m-%d %H:%M:%S")
    config.Hide_output = True
    config.Debug = True
    config.Count = True
    config.Pandas = True
    
    try: 
        twint.run.Search(config)
        
        csv = pandas.read_csv('./rose_output.csv')
        csv = csv.drop_duplicates()
        csv.to_json('{}.json'.format(coin), orient="records")
        tweets_from_csv = json.load(open('{}.json'.format(coin)))
        
        client = MongoClient("mongodb+srv://admin:change123@cluster0.ibw49.mongodb.net/Masterproject?retryWrites=true&w=majority")
        db = client.Masterprojekt
        tweets = db['tweets.{}'.format(coin)]
        tweets.insert_many(tweets_from_csv)
    except Exception as e:
        print(e)
    finally:        
        remove('{}_output.csv'.format(coin))
        remove('{}_resume.csv'.format(coin))
        remove('{}.json'.format(coin))
        


schedule.every().day.at("00:00").do(lambda: getTweets('Oasis Network OR $rose', 'rose'))
schedule.every().day.at("00:00").do(lambda: getTweets('Loopring OR lrc', 'loopring'))


while True:
    schedule.run_pending()
    time.sleep(60)

"""
cg = CoinGeckoAPI()
pprint(cg.get_price('loopring', vs_currencies='eur'))
"""

"""
from time import time, sleep
while True:
    sleep(60 - time() % 60)
	# thing to run
"""
