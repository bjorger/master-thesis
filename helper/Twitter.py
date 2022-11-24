import snscrape.modules.twitter as sntwitter
import pandas as pd
from TweetNormalizer import normalizeTweet

import re
from typing import Dict

def remove_from_dict(tweet: Dict, keys_to_remove: Dict) -> Dict:
    for key in keys_to_remove:
        del tweet[key]
    
    return tweet

def scrap_tweets(ticker: str, currency: str, since: str) -> pd.DataFrame:
    tweet_keys_to_remove = ['cashtags', 'conversationId', 'coordinates', 'id', 'inReplyToTweetId', 'media', 'source', 'sourceLabel', 'tcooutlinks', 'url', 'outlinks', 'renderedContent']
    
    user_keys_to_remove = ['location', 'linkUrl', 'linkTcourl', 'profileImageUrl', 'profileBannerUrl']
    
    tweets = []
    users = []


    for i,tweet in enumerate(sntwitter.TwitterHashtagScraper('#{} since:{}'.format(currency, since)).get_items()):
        tweet = tweet.__dict__
        user = tweet['user'].__dict__
        
        tweet = remove_from_dict(tweet, tweet_keys_to_remove)
        user = remove_from_dict(user, user_keys_to_remove)
        #Remove mentions
        tweet['content'] = re.sub("@[A-Za-z0-9_]+","", tweet['content'])
        #Remove hashtags
        tweet['content'] = re.sub("#[A-Za-z0-9_]+","", tweet['content'])
        normalized = normalizeTweet(tweet['content'])
        tweet['normalized'] = normalized
        tweet['user'] = user['username']
    
        tweets.append(tweet)
        users.append(user)   
        
    for i,tweet in enumerate(sntwitter.TwitterHashtagScraper('#{} since:{}'.format(ticker.upper(), since)).get_items()):
        tweet = tweet.__dict__
        user = tweet['user'].__dict__
        
        tweet = remove_from_dict(tweet, tweet_keys_to_remove)
        user = remove_from_dict(user, user_keys_to_remove)
        #Remove mentions
        tweet['content'] = re.sub("@[A-Za-z0-9_]+","", tweet['content'])
        #Remove hashtags
        tweet['content'] = re.sub("#[A-Za-z0-9_]+","", tweet['content'])
        normalized = normalizeTweet(tweet['content'])
        tweet['normalized'] = normalized
        tweet['user'] = user['username']
    
        tweets.append(tweet)
        users.append(user)    
        
    tweets = pd.DataFrame(tweets) 
    tweets.reset_index(inplace=True)
    tweets.to_json('./data/tweets_test.json')
    tweets.to_csv('./data/tweets_test.csv', sep='\t')
    
    users = pd.DataFrame(users)
    users.reset_index(inplace=True)
    users.to_json('./data/users_test.json')
    users.to_csv('./data/users_test.csv', sep='\t')

scrap_tweets('loopring', 'lrc', '2022-11-23')