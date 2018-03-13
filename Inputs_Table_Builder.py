import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from Variable_Functions.Twitter_Sentiment import dates_to_sentiment
from crycompare import *
import subprocess






def db_connection(database):
    """"""
    db_connection = sqlite3.connect(database)
    return db_connection


def get_symbols(database):
    """"""
    db_connection = sqlite3.connect(database)
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name NOT LIKE '%_1%'")
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

    #split_symbols[symbol][0] is the "tp" symbol
    #split_symbols[symbol][1] is the "from" symbol

    return split_symbols




######################################### Main function to build input dataset #####################
def generate_input_dataset(database):
    """"""
    symbols = get_symbols(database)
    table_names = {}

    for symbol in symbols:
        table_names[symbol] = OLHCV_From_DB(symbol, database)
    i = len(symbols)
    for symbol in symbols:
        print(str(i) + " More Symbols to Pull Sentiment For")
        i -= 1
        sentiment_variables = twitter_sentiment(symbol, 1)
        print()
        table_names[symbol]['Tweet_Sentiment_Polarity'] = sentiment_variables[0]
        table_names[symbol]['Tweet_Sentiment_Subjectivity'] = sentiment_variables[1]
        table_names[symbol]['Tweet_Positive_Percent'] = sentiment_variables[2]
        table_names[symbol]['Tweet_Sentiment_STDDEV'] = sentiment_variables[3]
        table_names[symbol]['Tweet_Sentiment_Polarity_to'] = sentiment_variables[4]
        table_names[symbol]['Tweet_Sentiment_Subjectivity_to'] = sentiment_variables[5]
        table_names[symbol]['Tweet_Positive_Percent_to'] = sentiment_variables[6]
        table_names[symbol]['Tweet_Sentiment_STDDEV_to'] = sentiment_variables[7]
        table_names[symbol]['Tweet_Sentiment_Polarity_from'] = sentiment_variables[8]
        table_names[symbol]['Tweet_Sentiment_Subjectivity_from'] = sentiment_variables[9]
        table_names[symbol]['Tweet_Positive_Percent_from'] = sentiment_variables[10]
        table_names[symbol]['Tweet_Sentiment_STDDEV_from'] = sentiment_variables[11]

    return table_names




