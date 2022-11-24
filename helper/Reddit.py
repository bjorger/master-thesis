
# importing the requests library
import requests
import json
import time
import math
import datetime
import numpy as np
from datetime import timedelta
import praw
import pandas as pd

config = {
    "username" : "bjorgbirb",
    "client_id" : "-QdhQYEx5aOdyl-p-UfoVQ",
    "client_secret" : "Zu1RswYSAKjFVABFb7AUTsKuAhg7IQ",
    "user_agent" : "script:https://github.com/bjorger/master-thesis:v1.0.0 (by u/bjorgbirb)"
}
reddit = praw.Reddit(client_id = config['client_id'], \
                     client_secret = config['client_secret'], \
                     user_agent = config['user_agent'])

PUSH_SHIFT_URL = "https://api.pushshift.io/reddit/search/submission?subreddit={}&before={}&size=500"

response = requests.get(PUSH_SHIFT_URL.format("CryptoCurrency", "2h"))

response_json = json.loads(response.content)

print(response_json)

df = pd.DataFrame(response_json['data'])

print(df.keys())
print(df['id'])