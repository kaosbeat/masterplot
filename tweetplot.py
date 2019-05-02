import sys
import tweepy
from tweetkeys import *
  
# authentication 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret) 
   
api = tweepy.API(auth) 
tweet = sys.argv[1] # some text
image_path = sys.argv[2] # png
  
# to attach the media file 
#status = 
api.update_with_media(image_path, tweet)  
# api.update_status(status = tweet) 