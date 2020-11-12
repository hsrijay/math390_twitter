# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 18:10:49 2020

@author: harsh
"""

import pandas as pd
import numpy as np
from textblob import TextBlob
import re

#remove mismatches in replyDict and keyDict
for key in list(replyDict.keys()):
  if key not in tweetDict:
    del replyDict[key]
    
for key in list(tweetDict.keys()):
  if key not in replyDict:
    del tweetDict[key]

#remove tweets with only 1 reply
too_few_replies = []
for key in list(replyDict.keys()):
    if len(replyDict[key]) < 2:
        too_few_replies.append(key)
        del replyDict[key]
for key in list(tweetDict.keys()):
    if key in too_few_replies:
        del tweetDict[key]

#convert tweets and replies to dataframes
tweets = pd.DataFrame.from_dict(tweetDict, orient = "index")
replies = pd.DataFrame.from_dict(replyDict, orient = "index")

#reorder rows of replies dataframe to match tweet dataframe

replies = replies.reindex(tweets.index.values)

#combine tweets and replies
data = pd.concat([tweets, replies], axis=1)
data.columns = range(len(data.columns))


#clean up tweet and reply text
for i in range(len(data.columns)):
    data[i] = data[i].apply(cleanUpText)
    
#sentiment analysis function
def getTextPolarity(txt):
    return TextBlob(txt).sentiment.polarity

#generate sentiment analysis scores for each column
for j in range(len(data.columns)-1):
    data['Polarity_{}'.format(j)] = data[j+1].apply(getTextPolarity)


#aggregate sentiment scores and number of replies for each tweet into dictionary
sentiment_scores = {}
for k in range(len(data.index)):
    sentiment_scores[data.index[k]] = np.array((np.mean(data.iloc[k,:]['Polarity_0':'Polarity_{}'.format(len(replyDict[data.index[k]])-1)]), 
                                         len(replyDict[data.index[k]])))
                                               
#aggregate sentiment scores into weighted average for each category
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
#clean up the text of each category
for i in range(len(category_scores.index)):
    category_scores['Category'][i] = cleanUpText(category_scores['Category'][i])

#remove all nonalphanumeric characters, if necessary
#category_scores = category_scores[category_scores.Category.str.isalnum()]

#group values by category
category_scores = category_scores.groupby(category_scores['Category']).aggregate({'Score': 'mean'})


category_scores['Category'] = category_scores.index


category_scores.to_csv("mavs.csv")


  