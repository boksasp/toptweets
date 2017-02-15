from flask import Flask
from flask import render_template
from update_top_ten import get_toplist

app = Flask(__name__)

@app.route("/")
def index():
    toplist = get_toplist()
    return render_template("index.html", toplist=toplist)

if __name__ == "__main__":
    app.run()
