import twint
from pycoingecko import CoinGeckoAPI
from pprint import pprint
from datetime import datetime, timedelta
import schedule
import time

def test():
    print('test')

def getTweets(query: str, output_json: str, resume_json: str):
    print('Fetching tweets for query {}'.format(query))
    """
        Get time from yesterday at 00:00:00, to fetch all tweets within the last day
    """
    time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    config = twint.Config()
    config.Search = query
    config.Store_json = True
    config.User_full = True
    config.Output = '{}.json'.format(output_json)
    config.Resume = '{}.json'.format(resume_json)
    config.Since = time.strftime("%Y-%m-%d %H:%M:%S")
    config.Hide_output = True
    config.Debug = True
    config.Count = True
    
    try: 
        twint.run.Search(config)
    except Exception as e:
        print(e)

getTweets('Oasis Network OR $rose', 'rose_output', 'rose_resume')

#schedule.every().day.at("00:00").do(getTweets,'loopring OR lrc', 'loopring_output', 'loopring_resume')
"""
schedule.every().minute.do(getTweets,'Oasis Network OR $rose OR oasis network or $ROSE', 'loopring_output', 'loopring_resume')

while True:
    schedule.run_pending()
    time.sleep(60)
"""

cg = CoinGeckoAPI()
pprint(cg.get_price('loopring', vs_currencies='eur'))

"""
from time import time, sleep
while True:
    sleep(60 - time() % 60)
	# thing to run
"""
