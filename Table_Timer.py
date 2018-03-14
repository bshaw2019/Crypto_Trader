from Inputs_Table_Builder import *
import time
import datetime
import sqlite3
import pandas

starttime=time.time()

#Runs the Input Table Builder module in 5 minute timesteps, appending to database
while True:
  ts = time.time()
  ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  print("Scraping at: " + ts)
  input_tables = generate_input_dataset('databases/market_prices.db')
  db_connection = sqlite3.connect('databases/market_prices.db')
  cursor = db_connection.cursor()
  i = len(symbols)
  for symbol in symbols:
    split=symbol.split('/')
    try:
      cursor.execute("select Tweet_Sentiment_Polarity_to from '" + symbol + "';")
    except:
      cursor.execute("Alter table '" + symbol + "' RENAME TO " + split[0] + split[1] + "_1old")
    try:
      input_tables[symbol]['Tweet_Sentiment_Polarity']
    except:
      input_tables[symbol]['Tweet_Sentiment_Polarity'] = 0
    try:
      input_tables[symbol]['Tweet_Sentiment_Subjectivity']
    except:
      input_tables[symbol]['Tweet_Sentiment_Subjectivity'] = 0
    try:
      input_tables[symbol]['Tweet_Positive_Percent']
    except:
      input_tables[symbol]['Tweet_Positive_Percent'] = 0
    try:
      input_tables[symbol]['Tweet_Sentiment_STDDEV']
    except:
      input_tables[symbol]['Tweet_Sentiment_STDDEV'] = 0

    try:
      input_tables[symbol]['Tweet_Sentiment_Polarity_to']
    except:
      input_tables[symbol]['Tweet_Sentiment_Polarity_to'] = 0
    try:
      input_tables[symbol]['Tweet_Sentiment_Subjectivity_to']
    except:
      input_tables[symbol]['Tweet_Sentiment_Subjectivity_to'] = 0
    try:
      input_tables[symbol]['Tweet_Positive_Percent_to']
    except:
      input_tables[symbol]['Tweet_Positive_Percent_to'] = 0
    try:
      input_tables[symbol]['Tweet_Sentiment_STDDEV_to']
    except:
      input_tables[symbol]['Tweet_Sentiment_STDDEV_to'] = 0
    try:
      input_tables[symbol]['Tweet_Sentiment_Polarity_from']
    except:
      input_tables[symbol]['Tweet_Sentiment_Polarity_from'] = 0
    try:
      input_tables[symbol]['Tweet_Sentiment_Subjectivity_from']
    except:
      input_tables[symbol]['Tweet_Sentiment_Subjectivity_from'] = 0
    try:
      input_tables[symbol]['Tweet_Positive_Percent_from']
    except:
      input_tables[symbol]['Tweet_Sentiment_STDDEV_from'] = 0
    try:
      input_tables[symbol]['Tweet_Sentiment_STDDEV_from']
    except:
      input_tables[symbol]['Tweet_Sentiment_STDDEV_from'] = 0
    input_tables[symbol].to_sql(name=(str(symbol)), con=db_connection, if_exists = 'append', index=False)
ts = time.time()

time.sleep(300.0 - ((time.time() - starttime) % 300.0))
ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print("Saved to database at: " + ts)
print(input_tables)
