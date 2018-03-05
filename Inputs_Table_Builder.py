import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from Variable_Functions.Twitter_Sentiment import dates_to_sentiment
from crycompare import *



def db_connection(database):
    """"""
    db_connection = sqlite3.connect(database)
    return db_connection


def get_symbols(database):
    """"""
    db_connection = sqlite3.connect(database)
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    symbols1 = cursor.fetchall()
    symbols = []
    for symbol in symbols1:
        symbols.append(symbol[0])
    return symbols


symbols = get_symbols('databases/market_prices.db')

######################################## Bid Ask Spread Time #######################################
def OLHCV_From_DB(symbol, database):
    """"""
    df = pd.read_sql(r"SELECT * FROM '" + symbol + "'", con=db_connection(database))
    return df


######################################### Twitter Sentiment #######################################
def twitter_sentiment(symbol, max_tweets):
    """"""
    now = datetime.now()
    dates = [now.strftime("%Y-%m-%d")]
    sentiment_variables = dates_to_sentiment(dates, symbol, max_tweets)
    return sentiment_variables


######################################### Split Trading Pair into 'to' and 'from' ###########
def split_symbols(symbols):
    """"""
    split_symbols = {}
    for symbol in symbols:
        split_symbols[symbol] = symbol.split('/')

    from_coins = {}
    to_coins = {}

    for symbol in symbols:
        from_coins[symbol] = split_symbols[symbol][0]
        to_coins[symbol] = split_symbols[symbol][1]


######################################### Main function to build input dataset #####################
def generate_input_dataset(database):
    """"""
    symbols = get_symbols(database)
    table_names = {}

    for symbol in symbols:
        table_names[symbol] = OLHCV_From_DB(symbol, database)

    for symbol in symbols:
        sentiment_variables = twitter_sentiment(symbol, 50)
        table_names[symbol]['Tweet_Sentiment_Polarity'] = sentiment_variables[0]
        table_names[symbol]['Tweet_Sentiment_Subjectivity'] = sentiment_variables[1]
        table_names[symbol]['Tweet_Positive_Percent'] = sentiment_variables[2]
        table_names[symbol]['Tweet_Sentiment_STDDEV'] = sentiment_variables[3]

    return table_names

input_tables = generate_input_dataset('databases/market_prices.db')
print(input_tables)
