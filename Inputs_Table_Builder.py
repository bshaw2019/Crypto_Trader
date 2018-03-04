import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from Variable_Functions.Twitter_Sentiment import dates_to_sentiment


db_connection = sqlite3.connect('databases/market_prices.db')


######################################## Bid Ask Spread Time #######################################
def OLHCV_From_DB(symbol):
	df = pd.read_sql(r"SELECT * FROM '" + symbol + "'", con=db_connection)
	return df


######################################### Twitter Sentiment ##########################
def twitter_sentiment(symbol, max_tweets):

	now = datetime.now() 
	dates = [now.strftime("%Y-%m-%d")]
	sentiment_variables = dates_to_sentiment(dates, symbol, max_tweets)
	return sentiment_variables





table_names = {}
symbols = ['ETH/BTC', 'LTC/BTC']

for symbol in symbols:
	table_names[symbol] = OLHCV_From_DB(symbol)

for symbol in symbols:
	sentiment_variables = twitter_sentiment(symbol, 100)
	table_names[symbol]['Tweet_Sentiment_Polarity'] = sentiment_variables[0]
	table_names[symbol]['Tweet_Sentiment_Subjectivity'] = sentiment_variables[1]
	table_names[symbol]['Tweet_Positive_Percent'] = sentiment_variables[2]
	table_names[symbol]['Tweet_Sentiment_STDDEV'] = sentiment_variables[3]

for symbol in symbols:
	print(symbol)
	print(table_names[symbol])

