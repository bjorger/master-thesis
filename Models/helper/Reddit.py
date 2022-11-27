
# importing the requests library
import requests
import json
import time
import math
import numpy as np
from datetime import timedelta
import praw
import pandas as pd
from pmaw import PushshiftAPI
import datetime as dt

config = {
    "username" : "bjorgbirb",
    "client_id" : "-QdhQYEx5aOdyl-p-UfoVQ",
    "client_secret" : "Zu1RswYSAKjFVABFb7AUTsKuAhg7IQ",
    "user_agent" : "script:https://github.com/bjorger/master-thesis:v1.0.0 (by u/bjorgbirb)"
}

reddit = praw.Reddit(client_id = config['client_id'], \
                     client_secret = config['client_secret'], \
                     user_agent = config['user_agent'])

api = PushshiftAPI()
before = int(dt.datetime(2021,2,1,0,0).timestamp())
after = int(dt.datetime(2020,12,1,0,0).timestamp())

subreddit="wallstreetbets"
limit=100000
submissions = api.search_submissions(subreddit=subreddit, limit=limit, before=before, after=after)
print(f'Retrieved {len(submissions)} submissions from Pushshift')