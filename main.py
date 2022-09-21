import schedule
import time
import os
from data_collector import DataCollector
from dotenv import load_dotenv

load_dotenv()
 
dataCollector = DataCollector()


schedule.every().monday.at("00:00").do(lambda: dataCollector.fetchTweets('$stx OR #stx', 'stacks'))
schedule.every().monday.at("00:00").do(lambda: dataCollector.fetchTweets('$lrc OR #lrc', 'loopring'))    
schedule.every(30).minutes.do(lambda: dataCollector.fetchPrice(os.environ.get("LRC_TICKER")))
schedule.every(30).minutes.do(lambda: dataCollector.fetchPrice(os.environ.get("STX_TICKER")))
schedule.every(30).minutes.do(lambda: dataCollector.fetchPrice(os.environ.get("BTC_TICKER")))
schedule.every().day.at("00:00").do(lambda: dataCollector.fetchFearAndGreedIndex())

while True:
    schedule.run_pending()
    time.sleep(1)