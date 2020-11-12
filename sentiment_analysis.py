# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 18:10:49 2020

@author: harsh
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
import re

for key in list(replyDict.keys()):
  if key not in tweetDict:
    del replyDict[key]
    
for key in list(tweetDict.keys()):
  if key not in replyDict:
    del tweetDict[key]
    
too_few_replies = []
for key in list(replyDict.keys()):
    if len(replyDict[key]) < 2:
        too_few_replies.append(key)
        del replyDict[key]
for key in list(tweetDict.keys()):
    if key in too_few_replies:
        del tweetDict[key]


tweets = pd.DataFrame.from_dict(tweetDict, orient = "index")
replies = pd.DataFrame.from_dict(replyDict, orient = "index")

x = tweets.index.values
replies = replies.reindex(x)

data = pd.concat([tweets, replies], axis=1)
data.columns = range(117)

#clean up tweets
def cleanUpTweet(txt):
    # Remove mentions
    txt = re.sub(r'@[A-Za-z0-9_]+', '', str(txt))
    # Remove hashtags
    txt = re.sub(r'#', '', str(txt))
    # Remove retweets:
    txt = re.sub(r'RT : ', '', str(txt))
    # Remove urls
    txt = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', str(txt))
    txt = re.sub(r',', "", str(txt))
    txt = re.sub(r'\.', "", str(txt))
    txt = re.sub(r'\'s', "", str(txt))
    txt = re.sub(r':', "", str(txt))
    
    regrex_pattern = re.compile(pattern="["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)
    txt = regrex_pattern.sub(r'', txt)

    # txt = txt.strip('\n')
    txt = txt.strip()
    return txt

cleaned_data = data
for i in range(len(cleaned_data.columns)):
    cleaned_data[i] = cleaned_data[i].apply(cleanUpText)
    

def getTextPolarity(txt):
    return TextBlob(txt).sentiment.polarity

for j in range(len(cleaned_data.columns)-1):
    cleaned_data['Polarity_{}'.format(j)] = cleaned_data[j+1].apply(getTextPolarity)


sentiment_scores = {}
for k in range(len(cleaned_data.index)):
    sentiment_scores[cleaned_data.index[k]] = np.array((np.mean(cleaned_data.iloc[k,:]['Polarity_0':'Polarity_{}'.format(len(replyDict[cleaned_data.index[k]])-1)]), 
                                         len(replyDict[cleaned_data.index[k]])))
                                               

category_scores = pd.DataFrame(columns = ['Category', 'Score'])
for i in range(len(categoriesDict)):
    score = 0
    total_replies = 0
    tweet_list = categoriesDict[list(categoriesDict.keys())[i]]
    for tweet in tweet_list:
        if tweet in list(sentiment_scores.keys()):
            score = score + (sentiment_scores[tweet][0] * sentiment_scores[tweet][1])
            total_replies = total_replies + sentiment_scores[tweet][1]
            category_scores = category_scores.append({'Category': list(categoriesDict)[i],
                                              'Score': score/total_replies}, ignore_index = True)
for i in range(len(category_scores.index)):
    category_scores['Category'][i] = cleanUpText(category_scores['Category'][i])

#category_scores = category_scores[category_scores.Category.str.isalnum()]

category_scores = category_scores.groupby(category_scores['Category']).aggregate({'Score': 'mean'})

category_scores = category_scores[category_scores.Score != 0]

category_scores['Category'] = category_scores.index

import plotly.express as px
px.scatter(category_scores, x="Score", y="Category",
                 title="Gender Earnings Disparity",
                 labels={"salary":"Annual Salary (in thousands)"} # customize axis label
                )

fig.show()

category_scores.to_csv("mavs.csv")


  