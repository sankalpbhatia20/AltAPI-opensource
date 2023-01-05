import pandas as pd
from datetime import datetime as dt
import urllib.request
import json


def esg_scores(asset):
    #dataframes = []
    url = "https://query2.finance.yahoo.com/v1/finance/esgChart?symbol={}".format(asset)

    connection = urllib.request.urlopen(url)

    data = connection.read()
    data_2 = json.loads(data)
    Formatdata = data_2["esgChart"]["result"][0]["symbolSeries"]
    Formatdata_2 = pd.DataFrame(Formatdata)
    Formatdata_2["timestamp"] = pd.to_datetime(Formatdata_2["timestamp"], unit="s")

    #ticker_list = ['AAPL'] * len(Formatdata_2)
    #Formatdata_2['ticker'] = ticker_list

    formatted_date_list = []
    for date_ in Formatdata_2['timestamp']:
        formatted_date_list.append(str(date_))

    Formatdata_2['date'] = formatted_date_list

    Formatdata_2.reset_index(inplace=True)
    Formatdata_2.set_index("date", inplace=True)

    del Formatdata_2['index']
    del Formatdata_2['timestamp']

    Formatdata_2 = Formatdata_2.loc[::-1]

    print(Formatdata_2)

    json_response = Formatdata_2.to_json(orient = 'index')
    final_json = json.loads(json_response)

    return final_json