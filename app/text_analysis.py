from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

def text_analysis(response):
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

    response_split_list = str(response).split('. ')

    print(response_split_list)

    tokens = tokenizer(response_split_list , padding = True, truncation = True, return_tensors='pt')
    #print(tokens)

    outputs = model(**tokens)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

    positive = predictions[:, 0].tolist()
    negative = predictions[:, 1].tolist()
    neutral = predictions[:, 2].tolist()

    table = {"sentence":response_split_list,
            "positive":positive,
            "negative":negative, 
            "neutral":neutral}
        
    df = pd.DataFrame(table, columns = ["sentence", "positive", "negative", "neutral"])

    avg_positive = df['positive'].mean()
    avg_negative = df['negative'].mean()
    avg_neutral = df['neutral'].mean()

    json_result = df.to_json(orient="records")
    text_analysis_json = json.loads(json_result)

    text_analysis_json.insert(0, {'overall_positive_score':avg_positive,
                                    'overall_negative_score':avg_negative,
                                    'overall_neutral_score':avg_neutral})

    return text_analysis_json