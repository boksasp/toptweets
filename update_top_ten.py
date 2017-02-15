from pymongo import MongoClient

def get_toplist():
    db = DbClient()

    top_dict = {}
    top_list = []

    # Generate the top 10 tweets based on favorite_count + retweet_count
    for tweet in db.get_tweets():
        score = tweet['favorite_count'] + tweet['retweet_count']
        min_score = 9999
        key = ""

        # Insert the first 10 tweets in the top 10 list, regardless of score
        if len(top_dict) <= 10:
            top_dict[tweet['id']] = score
        else:
            for k,v in top_dict.items():
                if v <= min_score:
                    min_score = v
                    key = k

        if score > min_score:
            print "popping {} from top list".format(key)
            top_dict.pop(key)
            print "adding {} to top list".format(tweet['id'])
            top_dict[tweet['id']] = score

    # Insert the score and tweet in a dictionary to sort the list based on score
    # There can't be a simpler and more elegant way of doing this /s
    for id_str,score in top_dict.items():
        top_list.append([score, db.tweets.find_one({"id" : id_str})])

    top_list.sort(reverse=True)
    return top_list


class TopList(object):
    
    def generate_toplist(self, tweets):
        pass

    def is_topten(self, tweet):
        pass
    
    def insert(self, tweet):
        pass

class DbClient(object):
    
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.toptweetsDB

    def get_tweets(self):
        return self.db.tweets.find()