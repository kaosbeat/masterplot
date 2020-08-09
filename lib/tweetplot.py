import sys
import tweepy
from tweetkeys import *
from wand.image import Image


# ## get ourselves the image we need (convert svg to jpg)
# with Image(filename=sys.argv[2]) as img:
#     img.format = 'jpeg'
#     img.save(filename='out.jpg')


  
# authentication 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret) 
   
api = tweepy.API(auth) 
tweet = sys.argv[1] # some text
image_path = "out2.jpg" # jpg created above or in plotrender.py
print(image_path)
# to attach the media file 
#status = 
api.update_with_media(image_path, tweet)  
# api.update_status(status = tweet) 