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
    db = client.tweets
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
posts = db.posts

inserts = 0
for status in statuses:
    url = "https://twitter.com/i/web/status/{}".format(status.id_str)

    post = {"created_at": status.created_at,
            "favorite_count": status.favorite_count,
            "full_text": status.full_text,
            "lang": status.lang,
            "retweet_count": status.retweet_count,
            "text": status.text,
            "id" : status.id_str,
            "url" : url}

    if (posts.find({"id" : status.id_str}).count() > 0) or (status.text.__getslice__(0,4) == "RT @"):
        pass
    else:
        posts.insert_one(post)
        inserts += 1

print "Inserted {:d} unique tweets".format(inserts)
