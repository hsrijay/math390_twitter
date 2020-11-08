# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 13:59:33 2020

@author: harsh
"""

import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import sys

twitterApiKey = 'a'
twitterApiSecret = 'b'
twitterApiAccessToken = 'c'
twitterApiAccessTokenSecret = 'd'

auth = tweepy.OAuthHandler(twitterApiKey, twitterApiSecret)
auth.set_access_token(twitterApiAccessToken, twitterApiAccessTokenSecret)
twetterApi = tweepy.API(auth, wait_on_rate_limit = True)

#store tweets in df data frame
twitterAccount = "dallasmavs"

tweets = tweepy.Cursor(twetterApi.user_timeline, 
                        screen_name=twitterAccount, 
                        count=None,
                        since_id=None,
                        max_id=None,
                        trim_user=True,
                        exclude_replies=True,
                        contributor_details=False,
                        include_entities=False
                        ).items(50)

df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweet'])

#clean up tweets
def cleanUpTweet(txt):
    # Remove mentions
    txt = re.sub(r'@[A-Za-z0-9_]+', '', txt)
    # Remove hashtags
    txt = re.sub(r'#', '', txt)
    # Remove retweets:
    txt = re.sub(r'RT : ', '', txt)
    # Remove urls
    txt = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', txt)
    return txt

og = df
df['Tweet'] = df['Tweet'].apply(cleanUpTweet)

#sentiment analysis scores of tweets itself
def getTextSubjectivity(txt):
    return TextBlob(txt).sentiment.subjectivity

def getTextPolarity(txt):
    return TextBlob(txt).sentiment.polarity
df['Subjectivity'] = df['Tweet'].apply(getTextSubjectivity)
df['Polarity'] = df['Tweet'].apply(getTextPolarity)



#scrape comments
    
name = "dallasmavs"
replies = []
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)  
for full_tweets in tweepy.Cursor(twetterApi.user_timeline,screen_name = name,timeout=999999).items(2):
    index = 0
    for tweet in tweepy.Cursor(twetterApi.search,q='to:'+name,result_type='recent',timeout=999999).items(1000):
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
                replies.append(tweet.text)
    print("Tweet :",full_tweets.text.translate(non_bmp_map))
    for elements in replies:
        print("Replies :",elements)
    index = index + 1
    replies.clear()