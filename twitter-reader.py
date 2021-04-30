from datetime import datetime
import tweepy
import json
import csv
import requests

# Twitter APIs keys
# Ksjc8l6Twa2FngctK7mXRJZTw
# Twitter API key secret
# fgO0Cji6HQvm4fONlfdDtcngvjtEwupLpqg6Uu22qwfp7yt7cN
# Acess token 551739406-R145ECVVtt8aG363GG77P8Tpp1emsyJ9n918T0iD
# Acess token secret mgR5Iy1r4J28DyTEIhab1ReNU3juwj67FvELq3jEArgjg
#  Bearer token AAAAAAAAAAAAAAAAAAAAACkvLAEAAAAAGtWB2PiSoYHyTiYPphDgLu2W6Rg%3DW4zqvtjICjSbjx2XJ1xAmRfkVIoshlwqMgRuS997aKSfXH8DHf
# Authenticate to Twitter

CONSUMER_KEY = 'Ksjc8l6Twa2FngctK7mXRJZTw'
CONSUMER_SECRET = 'fgO0Cji6HQvm4fONlfdDtcngvjtEwupLpqg6Uu22qwfp7yt7cN'
ACCESS_TOKEN = "551739406-R145ECVVtt8aG363GG77P8Tpp1emsyJ9n918T0iD"
ACCESS_TOKEN_SECRET = 'mgR5Iy1r4J28DyTEIhab1ReNU3juwj67FvELq3jEArgjg'

# Authenticate to Twitter

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)  # test authentication

ids = []


def add_tweet_to_database(tweet):
    url = "http://localhost:4000/tweets/"
    payload = {
        "tags": tweet.tags,
        "date": tweet.date.strftime("%Y-%m-%dT%H:%M"),
        "author": tweet.author,
        "tweet_text": tweet.tweet_text,
        "url": tweet.url,
        "tweet_id": tweet.tweet_id,
        "question_id": tweet.question_id
    }
    headers = {
        'Content-Type': 'application/json'
    }

    requests.request("POST", url, headers=headers, data=json.dumps(payload, indent=4))


def add_source_to_database(source):
    url = "http://localhost:4000/source/"
    payload = {
        "tags": source.tags,
        "date": source.date.strftime("%Y-%m-%d"),
        "url": source.url,
        "site_name": source.site_name,
        "author": source.author,
        "description": source.description
    }
    headers = {
        'Content-Type': 'application/json'
    }

    requests.request("POST", url, headers=headers, data=json.dumps(payload, indent=4))


# Setting up a class for the tweets to make it much simpler to update the values thoughtout the program,
# as the values gets found
class Tweet:
    tags = []
    date = ""
    author = ""
    tweet_text = ""
    url = ""
    question_id = ""
    tweet_id = ""


class Source:
    tags = ""
    url = ""
    site_name = ""
    author = ""
    description = ""
    date = ""


# dict to store key value pair, where the key is the tweet id, and the value is the tweet object.
# Makes it possible to later on access the same object and assign new values to it
tweet_list = {}

with open('subreddit12.csv', 'r') as file:
    for line in csv.DictReader(file):
        url = line['url']
        if 'twitter' in url:
            tweet = Tweet()
            tweet.url = url
            tweet_id = url.split('/')[-1]
            tweet.tweet_id = tweet_id
            new_dict = {tweet.tweet_id, tweet}
            tweet_list[tweet_id] = tweet
            ids.append(tweet_id)
            tweet.tags = {"tag": line['tag'], 'weight': 1}
        if 'nasaspaceflight' in url:
            source = Source()
            source.url = url
            source.description = line["comment"]
            source.author = "NASASpaceflight"
            source.site_name = "forum.nasaspaceflight.com"
            source.tags = {"tag": line['tag'], 'weight': 1}
            date = line['date'].replace("'", "")
            source.date = datetime.strptime(date, "%Y-%m-%d")
            add_source_to_database(source)

# A call to the twitter api that look for a list of ids and returns a list of tweets and their information.
tweets = api.statuses_lookup(ids, tweet_mode="extended")

for tweet in tweets:
    current_tweet = tweet_list[tweet.id_str]
    if tweet.in_reply_to_status_id:
        question = api.statuses_lookup([tweet.in_reply_to_status_id_str], tweet_mode="extended")
        current_tweet.question_id = question[0].id_str
    current_tweet.date = tweet.created_at
    current_tweet.author = tweet.user.name
    current_tweet.tweet_text = tweet.full_text
    add_tweet_to_database(current_tweet)
