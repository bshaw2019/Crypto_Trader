import got3
import arrow
from textblob import TextBlob
import numpy as np


def dates_to_sentiment(dates, ticker, max_tweets):

    ticker = "$" + ticker

    sentiments = []
    positives = []
    negatives = []

    for d in dates:
        arrow_date = arrow.get(d)
        tweetCriteria = got3.manager.TweetCriteria().setQuerySearch("{}{}".format("#", ticker)).setMaxTweets(max_tweets) \
            .setSince(arrow_date.replace(days=1).format("YYYY-MM-DD")) \
            .setUntil(arrow_date.replace(days=2).format("YYYY-MM-DD"))
        tweets = got3.manager.TweetManager.getTweets(tweetCriteria)

        sents_per_date = []

        for t in tweets:
            blob = TextBlob(t.text)
            sent = blob.sentiment[0] #get the polarity (subjectivity seems less important)
            sents_per_date.append(sent)
            if blob.sentiment[0] > 0:
                positives.append(t)
            else:
                negatives.append(t)

        mean_sentiment = sum(sents_per_date) / len(sents_per_date)

        sentiments.append(mean_sentiment)





        # #warning insight
        # try:
        #     sentiments.append(sents_per_date.mean())
        # except RuntimeWarning:
        #     print("RUNTIME WARNING")
        #     print(d)
        #     print(sents_per_date)
        #     for t in tweets:
        #         print(t.text)

    sentiments = np.asarray(sentiments)

    return sentiments


##UNIT TEST
#dates = ['2017-08-01']
#ticker = '$BTC/USDT'
#max_tweets = 100
#print(dates_to_sentiment(dates, ticker, max_tweets))