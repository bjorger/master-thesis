from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyzeTweet(tweet: dict) -> dict:
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