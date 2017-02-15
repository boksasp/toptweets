from pymongo import MongoClient

def get_toplist():
    client = MongoClient()
    db = client.tweets
    top_posts = db.top_posts

    top_dict = {}
    top_list = []

    # Generate the top 10 tweets based on favorite_count + retweet_count
    for post in db.posts.find():
        score = post['favorite_count'] + post['retweet_count']
        min_score = 9999
        key = ""

        # Insert the first 10 posts in the top 10 list, regardless of score
        if len(top_dict) <= 10:
            top_dict[post['id']] = score
        else:
            for k,v in top_dict.items():
                if v <= min_score:
                    min_score = v
                    key = k

        if score > min_score:
            print "popping {} from top list".format(key)
            top_dict.pop(key)
            print "adding {} to top list".format(post['id'])
            top_dict[post['id']] = score

    # Insert the score and post in a dictionary to sort the list based on score
    # There can't be a simpler and more elegant way of doing this /s
    for id_str,score in top_dict.items():
        top_list.append([score, db.posts.find_one({"id" : id_str})])

    top_list.sort(reverse=True)
    return top_list
