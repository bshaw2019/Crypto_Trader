# Crypto_Trader
**A Live Machine-Learning based Cryptocurrency Trader for the Poloniex Exchange**

If you would like to follow our progress or reach out to developers, feed free to join our discord channel at:
https://discord.gg/UPNV2fH

The goal of the project is to create an open sourced, machine learning based cryptocurrency portfolio optimizer including as many relevant variables as possible. 

These will include:

- **Community Sentiment** (such as forum and twitter sentiment analysis)
- **Analyst Opinions** (notable twitter account/analyst feeds with a history of winning strategies - ex. "Haejin" a successful elliot wave trader with an established history)
- **Global Economic Indexes** (DOW, Nikkei225, FOREX data, etc.)
- **Open/Close/High/Low/Volume**
- **Live Orderbook Data** (spread, bid, ask, order size) 
- **Technical Indicators** (MACD's, MA's, VWAPS, etc.)
- **Any Other Variable** of interest found to be important (Please feel free to brainstorm and send suggestions)


A **Boruta Analysis** (variation of Random forest) will be used to reduce these input variables by removing "unimportant" features. 

Using this input dataset, a machine learning **Binary Classifier** will be created to assign trading pairs on Poloniex a confidence score from 0 to 1. This value will represent the confidence that the trading pair will increase over a certain timeframe. Multiple machines may be constructed to score for a 5 minute window, 10 minute, 15 minute, 30 minute, 1 hour, etc. 

Using these scores, a **Q-Learning Bot** ("reinforcement learning") will be created that will optimize a trading strategy based on the binary classifier scores. The machine will read the amount of capital in the users Poloniex Account, and automatically place trades to optimize the portfolios holdings. These strategies will use stop losses and sell limits. Because it is q learning based, the machine will receive, and use live data to make decisions in a live auto-updating context with a reward that optimizes profit. This will allow the machine to continue to train and optimize itself over time while feeding in live data and placing trades.


Ultimately, the program will have the ability to be run 24 hours a day while optimizing a portfolio using live data, while taking into account fees in order to identify and take advantage of all trading opportunities accross the entire cryptocurrency market on Poloniex. Because of the decimal based system of cryptocurrencies, in theory a portfolio of any size should be able to be used as long as the user has the minimum trade size on Poloniex.



| Major Design Features |         Purpose          |
| --------------------- |:------------------------:|
| Identified Variables  | Related to Price Action  |
| Data Scraper          | Live Variables to Array  |
| Binary Classifers     | Score Trading Pairs Live |
| Q-Learning Bot        | Optimize Trade Strategy  |
| Poloniex API Link     | Allow Bot to Make Trades |



If you would like to donate to the project, please do so at the following Bitcoin/Litecoin/Ethereum addresses. All donations appreciated :)

**DONATIONS**

| Currency |                  Address                   |
| -------- |:-----------------------------------------: |
| Bitcoin  |     1GjVgMUDfKHzhxgeauRagVfp1GCrSJXijb     |
| Litecoin | 0x9852389Bd431A90A9AEcb48EdA50Da1ac05Bd4d8 |
| Ethereum |     M9oJaUnCB6Soistk3wSETziFDzz8gAaJCU     |
    
