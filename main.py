import schedule
import time
import os
from data_collector import DataCollector
from dotenv import load_dotenv

load_dotenv()

lrc_ticker = os.environ.get("LRC_TICKER")
stx_ticker = os.environ.get("STX_TICKER")
dataCollector = DataCollector()

schedule.every().monday.at("00:00").do(lambda: dataCollector.fetchTweets('$stx OR #stx', 'stacks'))
schedule.every().monday.at("00:00").do(lambda: dataCollector.fetchTweets('$lrc OR #lrc', 'loopring'))    
schedule.every(30).minutes.do(lambda: dataCollector.fetchPrice(lrc_ticker))
schedule.every(30).minutes.do(lambda: dataCollector.fetchPrice(stx_ticker))
schedule.every().day.at("00:00").do(lambda: dataCollector.fetchFearAndGreedIndex())

while True:
    schedule.run_pending()
    time.sleep(1)