import twitter
from pymongo import MongoClient
from configobj import ConfigObj

def setup():

    config = ConfigObj("./toptweets.conf")
    api = twitter.Api(consumer_key=config['consumer_key'],
        consumer_secret=config['consumer_secret'],
        access_token_key=config['access_token_key'],
        access_token_secret=config['access_token_secret'])

    client = MongoClient()
    db = client.toptweetsDB
    return config, api, db

config, api, db = setup()

query = "l={}&q=%23{}%20since%3A{}%20until%3A{}&count={}".format(
        config['language'],
        config['hashtag'],
        config['since'],
        config['until'],
        config['count'])
        
statuses = api.GetSearch(raw_query=query)
print "Found {:d} tweets".format(len(statuses))
tweets = db.tweets

inserts = 0
for status in statuses:
    url = "https://twitter.com/i/web/status/{}".format(status.id_str)

    tweet = {"created_at": status.created_at,
            "favorite_count": status.favorite_count,
            "full_text": status.full_text,
            "lang": status.lang,
            "retweet_count": status.retweet_count,
            "text": status.text,
            "id" : status.id_str,
            "url" : url}

    if (tweets.find({"id" : status.id_str}).count() > 0) or (status.text.__getslice__(0,4) == "RT @"):
        pass
    else:
        tweets.insert_one(tweet)
        inserts += 1

print "Inserted {:d} unique tweets".format(inserts)
