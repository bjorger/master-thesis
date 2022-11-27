import snscrape.modules.twitter as sntwitter
import pandas as pd
from TweetNormalizer import normalizeTweet
from Analzyer import group_tweets_by_timewindow

import re
from typing import Dict

def remove_from_dict(tweet: Dict, keys_to_remove: Dict) -> Dict:
    for key in keys_to_remove:
        del tweet[key]
    
    return tweet

def scrap_tweets(ticker: str, currency: str, since: str) -> pd.DataFrame:
    tweet_keys_to_remove = ['cashtags', 'coordinates', 'inReplyToTweetId', 'media', 'source', 'sourceLabel', 'tcooutlinks', 'url', 'outlinks', 'renderedContent', 'sourceUrl']
    user_keys_to_remove = ['location', 'linkUrl', 'linkTcourl', 'profileImageUrl', 'profileBannerUrl']
    
    tweets = []
    users = []
    
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('{} since:{}'.format(currency, since)).get_items()):        
        tweet = tweet.__dict__
        user = tweet['user'].__dict__
                
        if tweet['lang'] != 'en':
            continue
        
        tweet = remove_from_dict(tweet, tweet_keys_to_remove)
        user = remove_from_dict(user, user_keys_to_remove)
        #Remove mentions
        tweet['content'] = re.sub("@[A-Za-z0-9_]+","", tweet['content'])
        #Remove hashtags
        tweet['content'] = re.sub("#[A-Za-z0-9_]+","", tweet['content'])
        normalized = normalizeTweet(tweet['content'])
        tweet['normalized'] = normalized
        #tweet['sentiment'] = analyzer.analyze_tweet(normalized)
        tweet['user'] = user['username']
    
        tweets.append(tweet)
        users.append(user)   
        
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('{} since:{}'.format(ticker.upper(), since)).get_items()):
        tweet = tweet.__dict__
        user = tweet['user'].__dict__
         
        if tweet['lang'] != 'en':
            continue
        
        tweet = remove_from_dict(tweet, tweet_keys_to_remove)
        user = remove_from_dict(user, user_keys_to_remove)
        #Remove mentions
        tweet['content'] = re.sub("@[A-Za-z0-9_]+","", tweet['content'])
        #Remove hashtags
        tweet['content'] = re.sub("#[A-Za-z0-9_]+","", tweet['content'])
        normalized = normalizeTweet(tweet['content'])
        tweet['normalized'] = normalized
        #tweet['sentiment'] = analyzer.analyze_tweet(normalized)
        tweet['user'] = user['username']
     

    for i,tweet in enumerate(sntwitter.TwitterHashtagScraper('#{} since:{}'.format(currency, since)).get_items()):        
        tweet = tweet.__dict__
        user = tweet['user'].__dict__
                
        if tweet['lang'] != 'en':
            continue
        
        tweet = remove_from_dict(tweet, tweet_keys_to_remove)
        user = remove_from_dict(user, user_keys_to_remove)
        #Remove mentions
        tweet['content'] = re.sub("@[A-Za-z0-9_]+","", tweet['content'])
        #Remove hashtags
        tweet['content'] = re.sub("#[A-Za-z0-9_]+","", tweet['content'])
        normalized = normalizeTweet(tweet['content'])
        tweet['normalized'] = normalized
        #tweet['sentiment'] = analyzer.analyze_tweet(normalized)
        tweet['user'] = user['username']
    
        tweets.append(tweet)
        users.append(user)   
        
    for i,tweet in enumerate(sntwitter.TwitterHashtagScraper('#{} since:{}'.format(ticker.upper(), since)).get_items()):
        tweet = tweet.__dict__
        user = tweet['user'].__dict__
         
        if tweet['lang'] != 'en':
            continue
        
        tweet = remove_from_dict(tweet, tweet_keys_to_remove)
        user = remove_from_dict(user, user_keys_to_remove)
        #Remove mentions
        tweet['content'] = re.sub("@[A-Za-z0-9_]+","", tweet['content'])
        #Remove hashtags
        tweet['content'] = re.sub("#[A-Za-z0-9_]+","", tweet['content'])
        normalized = normalizeTweet(tweet['content'])
        tweet['normalized'] = normalized
        #tweet['sentiment'] = analyzer.analyze_tweet(normalized)
        tweet['user'] = user['username']
     
        
    tweets = pd.DataFrame(tweets) 
    tweets.reset_index(inplace=True)
    tweets.to_json('./data/tweets.json')
    tweets.to_csv('./data/tweets.csv', sep='\t')
    
    users = pd.DataFrame(users)
    users.reset_index(inplace=True)
    users.to_json('./data/users.json')
    users.to_csv('./data/users.csv', sep='\t')

    group_tweets_by_timewindow(tweets)

scrap_tweets('loopring', 'lrc', '2022-09-22')