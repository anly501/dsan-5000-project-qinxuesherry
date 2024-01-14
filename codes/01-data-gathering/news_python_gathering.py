# %%
import requests
import json
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

# %%
baseURL = "https://newsapi.org/v2/everything?"
total_requests=2
verbose=True

# THIS CODE WILL NOT WORK UNLESS YOU INSERT YOUR API KEY IN THE NEXT LINE
API_KEY='2d25c9787bb043658f8060f491dd2251'

# %%
def get_content(topic):
    URLpost = {'apiKey': API_KEY,
                'q': '+'+topic,
                'sortBy': 'relevancy',
                'totalRequests': 1}

    print(baseURL)
        # print(URLpost)

        #GET DATA FROM API
    response = requests.get(baseURL, URLpost) #request data from the server
        # print(response.url);  
    response = response.json() #extract txt data from request into json

        # PRETTY PRINT
        # https://www.digitalocean.com/community/tutorials/python-pretty-print-json

    print(json.dumps(response, indent=2))

        # #GET TIMESTAMP FOR PULL REQUEST
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d-H%H-M%M-S%S")

        # SAVE TO FILE 
    with open(timestamp+'-newapi-raw-data.json', 'w') as outfile:
        json.dump(response, outfile, indent=4)

# %%
get_content('Iphone')

# %%
def concatenate_article_content(article_dict):
    article_content = ''
    for article in article_dict.get('articles', []):
        article_title = str(article.get('title', ''))
        article_description = str(article.get('description', ''))
        content = article_title + article_description
        article_content += content
    return article_content

# %%
file_path = "iphone.json"

# Open the JSON file
with open(file_path, "r") as json_file:
    # Parse the JSON content into a dictionary
    iphone_dict = json.load(json_file)
iphone_content = concatenate_article_content(iphone_dict)
print(iphone_content)

# %%
text_file = open(r'iphone_content.txt', 'w')
text_file.write(iphone_content)
text_file.close()


