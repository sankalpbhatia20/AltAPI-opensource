import requests
import time
from bs4 import BeautifulSoup
from .config import settings

from dotenv import load_dotenv
import os

load_dotenv()


def text_summarization(top_url):
    # Send a GET request to the URL
    url = top_url
    
    # make a request to the URL
    response = requests.get(url)

    # parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # extract the text from the HTML content
    text = soup.get_text()

    # remove extra white space and new lines
    text_contents = " ".join(text.split())

    print(text_contents)

    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f'Bearer {settings.huggingface_token}'}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": text_contents,
    })

    time.sleep(10)

    print(output)

    try:
        return (output[0]['summary_text'])
    except Exception as e:
        print(e)
        return "We do not have access to summarize this URL"