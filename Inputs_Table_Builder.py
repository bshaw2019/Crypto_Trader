import sqlite3
import pandas as pd
import numpy as np

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

