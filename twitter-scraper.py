import tweepy
import json
import pandas as pd
from time import sleep

import datetime
import os
from textblob import TextBlob
import numpy as np

import json

#import twitter apps configaration file from config.py file
from config import keys as k


#OAUTH KEYS
CONSUMER_KEY=k.consumer_key
CONSUMER_SECRET=k.consumer_secret
ACCESS_TOKEN=k.access_token
ACCESS_TOKEN_SECRET=k.access_token_secret


#Class that has useful funcitions that can gain insight into specific users or tweets
class tweets():
    #sets the authentication of the Tweepy Api object
    def __init__(self, keys):
        auth=tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
        auth.set_access_token(keys.access_token, keys.access_token_secret)
        self.api=tweepy.API(auth)
    #gets the user information of the specific username
    def user_info(self, username):
        user=self.api.get_user(username)
        return user
    #gets the user information and then converts the User object into a JSON file.
    def user_info_json(self, username):
        user=self.api.get_user(username)
        f=open("user_info_data/"+username+"_userdata.json", "w")
        f.write(json.dumps(user._json))
    #searches for tweets based off of a search term.
    def search_for_tweets(self, search_term):
        search_results=self.api.search(q=search_term)
        return (search_results)
    #Calculates the amount of tweets per day for a specific username.
    def tweets_per_day(self, username):
        user=self.user_info(username)
        DAY = datetime.timedelta(1)
        d = datetime.date.today() - DAY
        tmpTweets=self.api.user_timeline(username)

        for tweet in tmpTweets:
            if tweet.created_at < endDate and tweet.created_at > startDate:
                tweets.append(tweet)
    #creates a list of statuses based off of a username and turns it JSON file.
    def create_status_data_json(self, username):
        max_id=self.api.user_timeline(username, count=1)[0].id
        count=100
        statuses=[]
        for i in range(0, 5):
            user_statuses=self.api.user_timeline(username, count=count, max_id=max_id)
            user_statuses_json=[s._json for s in user_statuses if "RT" in s.text]
            #santitize the data
            for status in list(user_statuses_json):
                for key in list(status.keys()):
                    if(status[key] == None):
                        status.pop(key, None)
            statuses=statuses+user_statuses_json
            # print("statuses: ", statuses)
            print("statuses length", len(statuses))
            print("max id: ", user_statuses[len(user_statuses)-1].id)
            print(count," retweets scraped")
            max_id=user_statuses[len(user_statuses)-1].id
            sleep(2)

        f=open("user_status_data/"+username+"_data.json", "w")
        f.write(json.dumps(user_statuses_json))

        return json.dumps(user_statuses_json)
    #gets the follower to following ratio of a specific user
    def follower_following_ratio(self, username):
        user=self.user_info(username)
        followers=user.followers_count
        friends=user.friends_count
        return (followers/friends)
    #Gets a list of followed accounts from a specific username
    def get_followers(self, username):
        ids=[]
        for page in tweepy.Cursor(self.api.followers_ids, screen_name=username).pages():
            ids.extend(page)
            sleep(5)
        return ids
    #Gets the list of followers from a specific username
    def get_friends(self, username):
        ids=[]
        for page in tweepy.Cursor(self.api.friends_ids, screen_name=username).pages():
            ids.extend(page)
            sleep(5)
        return ids
#Initialize the tweets object
t=tweets(k)

#WORKSPACE, the code here changes depending on what JSON file that was being written.

example_cases=[ 
  "Bonzo30507613",
  "JanSchm61866981",
  "ggarcia238",
  "MaeWest52499669",
  "Horam2017",
  "LisaLov80831185",
  "ChrisOBXnc",
  "HULSEYR7", 
  "kjbtazz", 
  "Tko77457444", 
  "godcountryfami2", 
  "BetsyGBJ9328", 
  "jolady42", 
]


for username in example_cases:
    print("STARTING ", username)
    outfile=open("friends_data/"+username+"_friends_data.json", "w")
    friends=t.get_friends(username)
    dataRow={username:friends}
    outfile.write(json.dumps(dataRow))
    sleep(10)
    


# bot requirments : Small amount of followers but large following
# Accounts that have a large following, but small amount of followers, and those followers also have a small amount of followers, but a large following. 
# If their account activity is mostly replies and retweets, but not likes.
# looking at its profile page and dividing the number of posts by the number of days it has been active. 705 posts per day, or almost one per minute for twelve hours at a stretch, every day for nine months. Strange patterns of activity are a defining characteristic
# Stock photos used frequently
# Handles are generated 
