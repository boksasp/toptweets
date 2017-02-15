## Web site for top 10 tweets

A python web site for displaying the top 10 tweets containing a hashtag of your choosing.  
The score for each tweet is retweets + likes.  
Tweets are stored in MongoDB.  

The project uses the following pip packages:  
* **python-twitter**
  * Python wrapper for the Twitter REST API
* **flask**
  * Web framework
* **configobj**
  * For reading config file
* **pymongo**
  * For working with MongoDB

### Authentication

This project uses Application-Only Authentication with the Twitter REST API.
### Setup

* Create a new app at [Twitter Apps](https://apps.twitter.com/)
  * Generate consumer token and secret for your app.
* Add your keys and access tokens for the Twitter REST API to **toptweets.conf**.
* Modify the Twitter Search API query string in **toptweets.py**, if needed.
  * Note that the Twitter Search API doesn't return anything for searches on dates further back than 7 days.
* Install MongoDB
* `python toptweets.py` populates the database with tweets, 100 at a time.

`python server.py` starts the web app.
