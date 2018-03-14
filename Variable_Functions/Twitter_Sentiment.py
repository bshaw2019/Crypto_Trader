import got3
import arrow
from textblob import TextBlob
import numpy as np
from termcolor import colored





def dates_to_sentiment(dates, ticker, max_tweets):

    ticker = ticker
    print(colored("Calculating sentiment for:" + ticker, 'white'))
    sentiments = []
    positives = []
    negatives = []
    arrow_date = dates
    tweetCriteria = got3.manager.TweetCriteria().setQuerySearch("{}{}".format("#", ticker)).setMaxTweets(max_tweets)
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

    try:
        sentiments.append(mean_polarity)
    except: 
        sentiments.append(0)
    #Mean Subjectivity 
    try:
        sentiments.append(mean_subjectivity)
    except: 
        sentiments.append(0)
    #Percentage of Tweets that are positive 
    try: 
        sentiments.append(percent_positive)
    except:
        sentiments.append(0.5)
    #Standard Deviation of tweet sentiment Polarity
    try: 
        sentiments.append(standard_deviation_polarity)
    except:
        sentiments.append(0)




    split_symbol = ticker.split('/')


    ticker = split_symbol[1]
    print(colored("Calculating sentiment for:" + ticker, 'red'))
    positives = []
    negatives = []
    subjectivity = []
    sents_per_date = []
    tweetCriteria = got3.manager.TweetCriteria().setQuerySearch("{}{}".format("#", ticker)).setMaxTweets(max_tweets) 
    tweets = got3.manager.TweetManager.getTweets(tweetCriteria)

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
        mean_polarity_from = sum(sents_per_date) / len(sents_per_date)
        mean_subjectivity_from = sum(subjectivity) / len(sents_per_date)
        percent_positive_from = len(positives) / len(sents_per_date)
        standard_deviation_polarity_from = np.std(standard_dev_array)
    else:
        mean_polarity_from = 0
        mean_subjectivity_from = 0
        percent_positive_from = .5
        standard_deviation_polarity_from = 0

    #Mean Polarity 
    try:
        sentiments.append(mean_polarity_from)
    except:
        sentiments.append(0)
    #Mean Subjectivity 
    try:
        sentiments.append(mean_subjectivity_from)
    except:
        sentiments.append(0)
    #Percentage of Tweets that are positive 
    try:
        sentiments.append(percent_positive_from)
    except:
        sentiments.append(0.5)        
    #Standard Deviation of tweet sentiment Polarity
    try:
        sentiments.append(standard_deviation_polarity_from)
    except:
        sentiments.append(0)




    ticker = split_symbol[0]
    print(colored("Calculating sentiment for:" + ticker, 'green'))
    positives = []
    negatives = []
    tweetCriteria = got3.manager.TweetCriteria().setQuerySearch("{}{}".format("#", ticker)).setMaxTweets(max_tweets)
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
        mean_polarity_to = sum(sents_per_date) / len(sents_per_date)
        mean_subjectivity_to = sum(subjectivity) / len(sents_per_date)
        percent_positive_to = len(positives) / len(sents_per_date)
        standard_deviation_polarity_to = np.std(standard_dev_array)
    else:
        mean_polarity_to = 0
        mean_subjectivity_to = 0
        percent_positive_to = .5
        standard_deviation_polarity_to = 0
    #Mean Polarity 
    try:
        sentiments.append(mean_polarity_to) 
    except:
        sentiments.append(0)
    #Mean Subjectivity 
    try:
        sentiments.append(mean_subjectivity_to)
    except:
        sentiments.append(0)
    #Percentage of Tweets that are positive 
    try:
        sentiments.append(percent_positive_to)
    except:
        sentiments.append(0.5)
    #Standard Deviation of tweet sentiment Polarity
    try:
        sentiments.append(standard_deviation_polarity_to)
    except:
        sentiments.append(0)




    sentiments = np.asarray(sentiments)

    return sentiments