# -*- coding: utf-8 -*-
"""
Created on Mon May  6 11:53:09 2019

@author: aaronliu
"""
import tweepy           
import pandas as pd     
import numpy as np      
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
from credentials import *    # Allow us to use the keys as variables

# Fill these contants with personal key and token. 
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_SECRET = ""

# API's setup:
def twitter_setup():
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    # Return API with authentication:
    '''
    In Twitter, rate limits are divided into 15-minute intervals. 
    In 15 minutes you can send 180 requests at max. 
    '''
    # set wait_on_rate_limit=True to ignore rate limit
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

# Create an extractor object:
extractor = twitter_setup()
# Create a tweet list 
# Type account id in screen name
# Could only extract 200 tweets at most
tweets = extractor.user_timeline(screen_name="", count=200)
print("Number of tweets extracted: {}.\n".format(len(tweets)))

# Print the most recent 5 tweets :
print("5 recent tweets:\n")
for tweet in tweets[:100]:
    print(tweet.text)

# Print tweets on personal page
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
private_tweets = api.home_timeline()
for tweet in private_tweets:
    print (tweet.text)

# Print tweets on public page
# Type account id
public_tweets = api.user_timeline("", count=200)
for tweet in public_tweets:
    print (tweet.text)
    
# Search for accounts that have sent tweets including the key word we want
# Type account id in query
for tweet in tweepy.Cursor(api.search,q="").items(100):
    print('Tweet by: @' + tweet.user.screen_name)
    
   
#################################################################
############### Basic Analysis ##################################
#################################################################

# Create dataframe 
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
display(data.head(10))  

# Add some basic attributes:
data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['Retweets']    = np.array([tweet.retweet_count for tweet in tweets])

display(data.head(10))

# Extract the tweet with the highest Likes and the highest Retweets respectively
fav_max = np.max(data['Likes'])
rt_max  = np.max(data['Retweets'])
fav = data[data.Likes == fav_max].index[0]
rt  = data[data.Retweets == rt_max].index[0]
# Highest likes
print("The tweet with the highest likes is: \n{}".format(data['Tweets'][fav]))
print("Number of likes: {}".format(fav_max))
print("{} characters.\n".format(data['len'][fav]))
# Highest retweets
print("The tweet with the highest retweets is: \n{}".format(data['Tweets'][rt]))
print("Number of retweets: {}".format(rt_max))
print("{} characters.\n".format(data['len'][rt]))

# Create time series 
tlen = pd.Series(data=data['len'].values, index=data['Date'])
tfav = pd.Series(data=data['Likes'].values, index=data['Date'])
tret = pd.Series(data=data['Retweets'].values, index=data['Date'])

# Visualize Likes & retweets 
tfav.plot(figsize=(16,4), label="Likes", legend=True)
tret.plot(figsize=(16,4), label="Retweets", legend=True);

#################################################################
############### Sources Analysis ################################
#################################################################

# Obtain all possible sources
sources = []
for source in data['Source']:
    if source not in sources:
        sources.append(source)
      
# Print sources list
print("Creation of content sources:")
for source in sources:
    print("* {}".format(source))
    
# Create a numpy vector mapped to labels
percent = np.zeros(len(sources))
for source in data['Source']:
    for index in range(len(sources)):
        if source == sources[index]:
            percent[index] += 1
            pass
percent /= 100

# Draw pie chart
pie_chart = pd.Series(percent, index=sources, name='Sources')
pie_chart.plot.pie(fontsize=11, autopct='%.2f', figsize=(6, 6));
