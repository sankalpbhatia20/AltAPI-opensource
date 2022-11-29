from openbb_terminal.sdk import openbb
import pandas as pd
import json
import uuid

def insider_trades_data(asset):
    
    df = (openbb.stocks.ins.lins(asset))

    df.reset_index(inplace = True)

    asset_list = [asset] * len(df)
    columns = ['date' , 'position', 'transaction' , 'number_of_shares', 'cost', 'value' ,'total_number_of_shares' , 'insider_trader' , 'SEC_form_4']

    df.columns = columns

    df['asset'] = asset_list

    try:
        df.reset_index(inplace=True)
        #print(df)

        df = df[:20]

        result = df.to_json(orient="records")
        insider_trades_json = json.loads(result)
        
        return insider_trades_json
        
    except:
        return {"Error" : "Make sure you have entered a valid US stock ticker"}
