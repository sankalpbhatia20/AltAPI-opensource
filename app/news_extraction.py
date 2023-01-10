from time import strftime
import pandas as pd
import datetime as dt
from datetime import date
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import ssl

import uuid

from timeit import default_timer as timer

today = date.today()
user_date = today.today()
user_date = user_date.strftime("%m-%d-%Y")

def news(asset, start_date = user_date, end_date = user_date):
    #start_date = "11-04-2022"
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download('vader_lexicon') #required for Sentiment Analysis

    nltk.download('punkt')
    config = Config()
    config.request_timeout = 10

    #end_date = start_date

    try:
        if asset != '':
            #Extract News with Google News
            googlenews = GoogleNews(start = start_date, end = end_date)
            googlenews.search(asset)
            result = googlenews.result()
            #store the results
            df = pd.DataFrame(result)
            #print(df)
            top_url = (df["link"][0])

            list =[] #creating an empty list 
            for i in df.index:
                dict = {} #creating an empty dictionary to append an article in every single iteration
                article = Article(df['link'][i],config=config) #providing the link
                try:
                    article.download() #downloading the article 
                    article.parse() #parsing the article
                    article.nlp() #performing natural language processing (nlp)
                except Exception as e:
                    print('***FAILED TO DOWNLOAD***', article.url)
                    #continue
                    #continue
                    return {"Error" : e}
                    #return {"Error" : "No news has been published about {} today till now. Try again soon!".format(asset)}
                #storing results in our empty dictionary
                dict['Date']=df['date'][i] 
                dict['Media']=df['media'][i]
                dict['Title']=article.title
                dict['Article']=article.text
                dict['Summary']=article.summary
                dict['Key_words']=article.keywords
                #print(dict)
                list.append(dict)
            check_empty = not any(list)
            #print(check_empty)
            if check_empty == False:
                news_df=pd.DataFrame(list) #creating dataframe
        else:
            print('Error')
    except:
        return {"Error" : "No news has been published about {} today till now. Try again soon!".format(asset)}

    #Sentiment Analysis
    #start = timer()
    def percentage(part,whole):
        return 100 * float(part)/float(whole)

    #Assigning Initial Values
    positive = 0
    negative = 0
    neutral = 0
    #Creating empty lists
    news_list = []
    neutral_list = []
    negative_list = []
    positive_list = []

    print(news_df)
    #Iterating over the tweets in the dataframe
    try:
        for news in news_df['Summary']:
            news_list.append(news)
            analyzer = SentimentIntensityAnalyzer().polarity_scores(news)
            neg = analyzer['neg']
            neu = analyzer['neu']
            pos = analyzer['pos']
            comp = analyzer['compound']

            if neg > pos:
                negative_list.append(news) #appending the news that satisfies this condition
                negative += 1 #increasing the count by 1
            elif pos > neg:
                positive_list.append(news) #appending the news that satisfies this condition
                positive += 1 #increasing the count by 1
            elif pos == neg:
                neutral_list.append(news) #appending the news that satisfies this condition
                neutral += 1 #increasing the count by 1 
    except Exception as e:
        return {"Error: " + str(e)}
        #return {"Error":"No news available to run sentiment analysis on the asset entered"}

    try:
        positive = percentage(positive, len(news_df)) #percentage is the function defined above
        negative = percentage(negative, len(news_df))
        neutral = percentage(neutral, len(news_df))

    #Converting lists to pandas dataframe
        news_list = pd.DataFrame(news_list)
        neutral_list = pd.DataFrame(neutral_list)
        negative_list = pd.DataFrame(negative_list)
        positive_list = pd.DataFrame(positive_list)
    except:
        return {"Error":"No news available till now to run sentiment analysis on the {} entered".format(asset)}

    try:
        if len(positive_list) == 1:
            positivity_index = len(positive_list)
        else:
            positivity_index = (len(positive_list) / 10)
        if positivity_index > 0.5:
            sentiment = "positive"
        elif (positivity_index == 0.5):
            sentiment = "neutral"
        else:
            sentiment = "negative"
    except:
        return {"Error" : "No news to analyse for the given date"}

    # For URL Text extraction

    # Creating data dictionary and converting into JSON
    id = uuid.uuid1()

    x = {
        "id" : id.hex,
        "asset" : asset,
        "date" : start_date,
        "compound_positivity_score" : positivity_index,
        "compound_sentiment": sentiment,
        "top_url": top_url
        }

    return x