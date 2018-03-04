import got3
import arrow
from textblob import TextBlob
import numpy as np

def dates_to_sentiment(dates, ticker, max_tweets):

    ticker = ticker
    print("Calculating sentiment for:" + ticker)

    sentiments = []
    positives = []
    negatives = []

    for d in dates:
        arrow_date = arrow.get(d)
        tweetCriteria = got3.manager.TweetCriteria().setQuerySearch("{}{}".format("#", ticker)).setMaxTweets(max_tweets) \
            .setSince(arrow_date.replace(days=-1).format("YYYY-MM-DD")) \
            .setUntil(arrow_date.replace(days=+1).format("YYYY-MM-DD"))
        tweets = got3.manager.TweetManager.getTweets(tweetCriteria)
        sents_per_date = []
        subjectivity = []

        for t in tweets:
            blob = TextBlob(t.text)
            sent = blob.sentiment[0] #get the polarity
            subjectives = blob.sentiment[1] #get the subjectivity
            sents_per_date.append(sent) #Saving polarity to sents_per_date
            subjectivity.append(subjectives) #Saving subjectivity to subjectivity 

            if blob.sentiment[0] > 0: #Separating positive and negative tweets to lists
                positives.append(t)
            else:
                negatives.append(t)

        standard_dev_array = np.asarray(sents_per_date)

        if len(sents_per_date) >= 1:
            mean_polarity = sum(sents_per_date) / len(sents_per_date)
            mean_subjectivity = sum(subjectivity) / len(sents_per_date)
            percent_positive = len(positives) / len(sents_per_date)
            standard_deviation_polarity = np.std(standard_dev_array)
        else:
            mean_polarity = 0
            mean_subjectivity = 0
            percent_positive = .5
            standard_deviation_polarity = 0
        #Mean Polarity 
        sentiments.append(mean_polarity)
        #Mean Subjectivity 
        sentiments.append(mean_subjectivity)
        #Percentage of Tweets that are positive 
        sentiments.append(percent_positive)
        #Standard Deviation of tweet sentiment Polarity
        sentiments.append(standard_deviation_polarity)

    sentiments = np.asarray(sentiments)

    return sentiments