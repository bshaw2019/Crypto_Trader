from crycompare import *
import pandas as pd
import sqlite3

db_connection = sqlite3.connect('databases/market_prices.db')
cursor = db_connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
symbols1 = cursor.fetchall()
symbols = []
for symbol in symbols1:
	symbols.append(symbol[0])
print(symbols)

h = History()

from_coins = []
to_coins = []

df_dict = {}

for coin in coins:
    histo = h.histoMinute(coin,'USD')
    if histo['Data']:
        df_histo = pd.DataFrame(histo['Data'])
        df_histo['time'] = pd.to_datetime(df_histo['time'],unit='s')
        df_histo.index = df_histo['time']
        del df_histo['time']
        del df_histo['volumefrom']
        del df_histo['volumeto']
        
        df_dict[coin] = df_histo
        print(df_dict[coin])