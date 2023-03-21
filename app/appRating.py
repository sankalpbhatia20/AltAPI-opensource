from google_play_scraper import Sort, reviews_all, search, app, reviews
import pandas as pd
import requests
import json

def get_app_reviews(asset):

    query = asset  # replace with the name of the app you want to extract reviews from
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
    API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    response_list = []
    for comment in comments_list[:10]:
        output = query({
        "inputs": comment,
        })

        response_list.extend(output)
        #print(output)

    # Convert responses to dataframe
    print(response_list)

    test_df = pd.DataFrame(response_list)
    print(test_df)

    # print comments and their scores along with 
    df = pd.DataFrame(list(zip(comments_list, score_list)), columns =['Comments', 'Score'])

    print(df)
    avg_score = df['Score'].mean()
    print(avg_score)

    try:
        df.reset_index(inplace=True)
        #print(df)

        df = df[:20]

        result = df.to_json(orient="records")
        app_rating_json = json.loads(result)
        
        return app_rating_json
    except Exception as e:
        return {"Error" : str(e)}


get_app_reviews('zomato')