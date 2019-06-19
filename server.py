from flask import Flask
from flask import render_template
from update_top_ten import get_toplist
from configobj import ConfigObj

app = Flask(__name__)

def setup():

    config = ConfigObj("./toptweets.conf")
    return config['hashtag']

@app.route("/")
def index():
    toplist = get_toplist(hashtag)
    return render_template("index.html", toplist=toplist, hashtag=hashtag)

hashtag = setup()

if __name__ == "__main__":

    app.run()
