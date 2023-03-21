from google_play_scraper import Sort, reviews_all, search, app, reviews
import pandas as pd
import requests
import time
import json

def get_google_playstore_app_reviews(company):

    query = company  # replace with the name of the app you want to extract reviews from
    result = search(query) #, page=1)

    app_id = result[0]['appId']
    print(app_id)

    result, continuation_token = reviews(
        app_id,
        lang='en', # defaults to 'en'
        country='US', # defaults to 'us'
        sort=Sort.MOST_RELEVANT, # defaults to Sort.NEWEST
        count=100 # defaults to 100
    )

    result, _ = reviews(
    app_id,
    continuation_token=continuation_token # defaults to None(load from the beginning)
)

    result_length = len(result)

    i = 0
    comments_list = []
    score_list = []
    while i < result_length:
        comments_list.append(result[i]['content'])
        score_list.append(result[i]['score'])
        i += 1

    # Usign huginface API to get most positive and negative comments
    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    negative_score_list = []
    postive_score_list = []

    for comment in comments_list[:10]:
        output = query({
        "inputs": comment,
        })

        time.sleep(2)

        if (output[0][0]['label']) == 'NEGATIVE':
            negative_score_list.append(output[0][0]['score'])
            postive_score_list.append(output[0][1]['score'])
        else:
            negative_score_list.append(output[0][1]['score'])
            postive_score_list.append(output[0][0]['score'])

        print(output)

    # print comments and their scores along with 
    df = pd.DataFrame(list(zip(comments_list, score_list, postive_score_list, negative_score_list)), columns =['Comments', 'Score', 'PositiveScore', 'NegativeScore'])

    print(df)
    avg_score = df['Score'].mean()
    print(avg_score)

    # get the index of the row with the highest PositiveScore and the row with the highest NegativeScore
    most_positive_idx = df['PositiveScore'].idxmax()
    most_negative_idx = df['NegativeScore'].idxmax()

    # get the Comments column value of the rows with the highest PositiveScore and the highest NegativeScore
    most_positive_comment = df.loc[most_positive_idx, 'Comments']
    most_negative_comment = df.loc[most_negative_idx, 'Comments']

    print("Most positive comment:", most_positive_comment)
    print("Most negative comment:", most_negative_comment)

    print('')

    try:
        df.reset_index(inplace=True)
        #print(df)

        df = df[:20]

        result = df.to_json(orient="records")
        app_rating_json = json.loads(result)

        final_json = {
            'AppName': company,
            'AppID': app_id,
            'AverageScore': avg_score,
            'MostPositiveComment': most_positive_comment,
            'MostNegativeComment': most_negative_comment,
            'Reviews_and_Scores': app_rating_json
        }

        return final_json
    except Exception as e:
        return {"Error" : str(e)}