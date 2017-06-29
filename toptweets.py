import twitter
from pymongo import MongoClient
from configobj import ConfigObj
from os import sys

def setup():

    config = ConfigObj("./toptweets.conf")
    api = twitter.Api(consumer_key=config['consumer_key'],
        consumer_secret=config['consumer_secret'],
        access_token_key=config['access_token_key'],
        access_token_secret=config['access_token_secret'])

    client = MongoClient()
    
    return config, api, client.toptweetsDB

def save_tweet(tweet):
    replaces = 0
    inserts = 0
    
    result = db.tweets.find_one({"id" : tweet["id"]})
    
    if (status.text.__getslice__(0,4) == "RT @"):
        pass
    elif (result):
        db.tweets.replace_one({"id" : result["id"]}, tweet)
        replaces += 1
    else:
        db.tweets.insert_one(tweet)
        inserts += 1
    
    return replaces, inserts

config, api, db = setup()

query = "l={}&q=%23{}%20since%3A{}%20until%3A{}&count={}".format(
        config['language'],
        config['hashtag'],
        config['since'],
        config['until'],
        config['count'])
        
statuses = api.GetSearch(raw_query=query)

if (len(statuses) == 0):
    print "No results found"
    sys.exit()
else:
    print "Found {:d} tweets".format(len(statuses))

for status in statuses:
    tweet = {"created_at": status.created_at,
            "favorite_count": status.favorite_count,
            "full_text": status.full_text,
            "lang": status.lang,
            "retweet_count": status.retweet_count,
            "text": status.text,
            "id" : status.id_str,
            "url" : "https://twitter.com/i/web/status/{}".format(status.id_str)}

    replaces, inserts = save_tweet(tweet)

print "Replaced {:d} old tweet(s)".format(replaces)
print "Inserted {:d} new tweet(s)".format(inserts)
