import pandas as pd
import tensorflow as tf
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer 
from datetime import timedelta, datetime

class Analyzer():
    tokenizer: AutoTokenizer
    model: TFAutoModelForSequenceClassification    
    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained("rabindralamsal/finetuned-bertweet-sentiment-analysis")
        self.model = TFAutoModelForSequenceClassification.from_pretrained("rabindralamsal/finetuned-bertweet-sentiment-analysis")
    
    def analyze(self, tweets: pd.DataFrame):
        sentiments = []
        for i, tweet in tweets.iterrows():
            input = self.tokenizer.encode(tweet['content'], return_tensors='tf')
            output = self.model.predict(input)[0]
            prediction = tf.nn.softmax(output, axis=1).numpy()
            sentiment = np.argmax(prediction)
            sentiments.append(sentiment)
        tweets['sentiment'] = sentiments
        tweets.to_csv('analyzed_test.csv', sep=',')
        
    def analyze_tweet(self, tweet: str):
        input = self.tokenizer.encode(tweet, return_tensors='tf')
        output = self.model.predict(input)[0]
        prediction = tf.nn.softmax(output, axis=1).numpy()
        sentiment = np.argmax(prediction)
        return sentiment

months = {
    'January': 31,
    'February': 28,
    'March': 31,
    'April': 30,
    'May': 31,
    'June': 30,
    'July': 31,
    'August':31,
    'September':30,
    'October': 31,
    'November': 30,
    'December': 31,
}

def group_tweets_by_timewindow(tweets: pd.DataFrame) -> pd.DataFrame:
    tweets['date'] = pd.to_datetime(tweets['date'])
    tweets.set_index('date')
    tweets.index = tweets['date']
    startDate = pd.to_datetime('2022-09-21 23:30:00+00:00')
    tweets = tweets[tweets['date'] >= startDate]
    
    analyzer = SentimentIntensityAnalyzer()

    analyzed_tweets = pd.DataFrame(columns=['Timewindow', 'Sentiment', 'Volume'])

    for year in range(2022, datetime.now().year + 1):
        tweets_year = tweets[tweets['date'].dt.year == year]
        for month in months:
            tweets_month = tweets_year[pd.to_datetime(tweets_year['date']).dt.strftime('%B') == month]
            for day in range(1, months[month] + 1):
                tweets_day = tweets_month.loc[(tweets_month['date'].dt.day == day)]

                if (tweets_day.size == 0):
                    continue
                
                for i in range(1, 49):
                    start = str(timedelta(minutes=(i-1)*30))
                    end = str(timedelta(minutes=(i*30)-1, seconds=59))
                    current_tweets = tweets_day.between_time(start, end)
                    results_tweet = []
                    tweets_in_timeframe = []
                    for tweet in current_tweets.iterrows():
                        tweet_id = str(tweet[1]['id'])
                        if (tweet_id in tweets_in_timeframe):
                            continue

                        sentiment_result = analyzer.polarity_scores(tweet[1]['content'])
                        results_tweet.append(sentiment_result['compound'])
                        tweets_in_timeframe.append(tweet_id)
                    
                    sentiment = 0
                    volume = 0
                    timewindow = '{}-{}-{} {}-{}'.format(day, month, year, start, end)

                    if (len(results_tweet) > 0):
                        sentiment = sum(results_tweet) / len(results_tweet)
                        volume = len(results_tweet)
                    
                    entry = {
                        'Timewindow': timewindow,
                        'Sentiment': sentiment,
                        'Volume': volume,
                        'TweetIds': ','.join(tweets_in_timeframe)
                    }
                    analyzed_tweets = analyzed_tweets.append(entry, ignore_index=True)
                    
    analyzed_tweets.to_csv('data/analzyed.csv', sep=',')
        
