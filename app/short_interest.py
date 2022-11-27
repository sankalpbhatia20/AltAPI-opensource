# Import required modules
from datetime import date
from lxml import html
import requests
from random import randrange
import uuid

today = date.today()
start_date = today.today()
start_date = start_date.strftime("%m-%d-%Y")
 
def short_info(asset):
    # Request the page
    try:
        page = requests.get('https://www.benzinga.com/quote/{}/short-interest'.format(asset))

        tree = html.fromstring(page.content) 
        
        # Get element using XPath
        short_interest_perc_element = tree.xpath('/html/body/div[1]/div[3]/div/div[2]/div/div[2]/div[10]/div/div[2]/div[1]/div[2]/div/div/div')
        short_interest_perc = short_interest_perc_element[0].text

        short_interest_element = tree.xpath('/html/body/div[1]/div[3]/div/div[2]/div/div[2]/div[10]/div/div[2]/div[1]/div[1]/div/div/div')
        short_interest = short_interest_element[0].text

        days_to_cover_element = tree.xpath('/html/body/div[1]/div[3]/div/div[2]/div/div[2]/div[10]/div/div[2]/div[1]/div[3]/div/div/div')
        days_to_cover = days_to_cover_element[0].text

        id = uuid.uuid1()

        values = {
            "id": id.hex,
            "asset": asset,
            "date": start_date,
            "short_interest": short_interest,
            "short_interest_percentage": short_interest_perc,
            "days_to_cover": float(days_to_cover)
        }

    except:
        values = {"Error": "Please enter a valid US TICKER"}
        
    return values