from requests import get 
from bs4 import BeautifulSoup
from datetime import datetime
import pickle
from pathlib import Path
import pandas as pd
from GoogleNews import GoogleNews
from .base import Ticker

# url = 'https://api.stocktwits.com/api/2/streams/symbol/AAPL.json'
# for i in [message['body'] for message in get(url).json()['messages']]:
#     print(i)
#     print('*' * 50)

url = 'https://stocktwits.com/symbol/CCIV'
response = get(url)
soup = BeautifulSoup(response.content, 'lxml')
print(soup.find('div', {'class': 'st_21nJvQl st_2h5TkHM st_8u0ePN3 st_2mehCkH'}))

def adl(self):
    data = self.get_month_data()
    adl = 0.0
    for row in data.iterrows():
        adl += (((row['Close'] - row['Low']) - (['High'] - row['Close']))/(['High'] - row['Low'])) * row['Volume']
    
    return adl
