import sqlite3
import pandas as pd
import numpy as np

########################################OHLCV#######################################
#Connects to the scraped Database saves in the "databases" subdirectory
db = sqlite3.connect('databases/market_prices.db')
cursor = db.cursor()

#Querying the ETH/BTC Table from the database
cursor.execute("SELECT * FROM 'ETH" + "/" + "BTC';")
alist = cursor.fetchall()

#Pulls column names for the ETH/BTC table
cursor.execute("PRAGMA table_info('ETH" + "/" + "BTC');")
col_names = cursor.fetchall()

#Converting ETH/BTC data to a numpy array 
table_names = {}
data = np.array(alist)

#To Do: Make a loop that creates numpy arrays for all pairs
#Name them according to the pair name (Ex. ETH_BTC) so they can be called later by symbol 



from Variable_Functions import Twitter_Scanner

#########################################TWITTER SENTIMENT##########################
# creating object of TwitterClient Class
api = Twitter_Scanner.TwitterClient()

# calling function to get tweets
tweets = api.get_tweets(query = "\"BTC/USDT\"", count = 200)

# picking positive tweets from tweets
ptweets = [tweet for tweet in tweets if tweet['sentiment'] > 0]

# percentage of positive tweets
print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

# picking negative tweets from tweets
ntweets = [tweet for tweet in tweets if tweet['sentiment'] < 0]

# percentage of negative tweets
print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

# percentage of neutral tweets
print("Neutral tweets percentage: {} % \
    ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

# printing first 5 positive tweets
print("\n\nPositive tweets:")
for tweet in ptweets[:10]:
    print(tweet['text'])

# printing first 5 negative tweets
print("\n\nNegative tweets:")
for tweet in ntweets[:10]:
    print(tweet['text'])